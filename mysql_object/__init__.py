"""
mysql_object

Small library to make it easier to work with MySQL in Python.
"""

__version__ = "0.0.4"
__author__ = 'Dennis Iversen'
__credits__ = '10kilobyte.com'

from .mysql_object import MySQLObject, get_mysql_object
from .sql_query import SQLQuery