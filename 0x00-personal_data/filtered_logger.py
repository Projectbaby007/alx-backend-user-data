#!/usr/bin/env python3
"""Handling personal data with the logging module"""

from typing import List
import csv
import logging
import mysql.connector
import re
import os

# PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST")
    db = mysql.connector.connect(
        database=db_name if db_name else 'my_db',
        host=db_host if db_host else 'localhost',
        user=db_username if db_username else 'root',
        password=db_password if db_password else 'root'
    )

    return db


with open('user_data.csv', 'r') as f:
    PII_FIELDS: tuple = ()
    reader = csv.reader(f)
    fields = next(reader)
    PII = ['name', 'address', 'email', 'ssn', 'passport', 'dl',
           'cc', 'birth', 'dob', 'born', 'phone', 'telephone',
           'vin', 'username', 'password', 'mac', 'ip']
    for field in fields:
        if field in PII:
            if len(PII_FIELDS) < 5:
                PII_FIELDS += (field,)
            else:
                break


def get_logger() -> logging.Logger:
    """returns a logger for logging user data"""
    user_logger = logging.Logger("user_data")
    user_logger.setLevel(logging.INFO)
    user_logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_logger.addHandler(handler)
    return user_logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator,
                      field + "=" + redaction + separator, temp)
    return temp


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """inherits init from Formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        uses the format() method from parent and
        applies and extra filter with filter_datum()
        """
        log: logging.Formatter = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def main():
    """
    Use all the above functions
    to read from a database and log the
    rows from the 'users' table, filtering
    personal data.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM users;')
    rows = cursor.fetchall()

    logger = get_logger()
    field_names = [i[0] for i in cursor.description]

    for row in rows:
        message = ''
        for field in range(len(row)):
            message += f'{field_names[field]}={row[field]};'
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
