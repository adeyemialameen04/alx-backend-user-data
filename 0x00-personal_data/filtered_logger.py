#!/usr/bin/env python3
""" Filtered logger module """
import bcrypt
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Formatter method to format incoming logs """
        record = logging.Formatter.format(self, record)
        record = filter_datum(self.fields, self.REDACTION,
                              record, self.SEPARATOR)
        return record


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Function to return log message obfuscated """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


def get_logger() -> logging.Logger:
    """" a function to return logging.logger object """
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function to return mysql.connector object """
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', default="root")
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', default="")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', default="localhost")
    db = os.environ.get('PERSONAL_DATA_DB_NAME')
    connector = mysql.connector.connection.MySQLConnection(user=user,
                                                           host=host,
                                                           password=password,
                                                           database=db)
    return connector

def main():
    """ entry point """
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    fields = cursor.column_names
    logger = get_logger()
    for row in cursor:
        message = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        logger.info(message.strip())
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
