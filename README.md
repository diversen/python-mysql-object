# python mysql object

Simple Python MySQL CRUD and query tool

The main usage is probably if you don't use a ORM, but query the MySQL database directly - maybe using `mysql.connector`.

## Install mysql-migration

    pip install git+https://github.com/diversen/python-mysql-object

Or using a tag:

    pip install git+https://github.com/diversen/python-mysql-object@v0.0.1


## Usage

```python
from mysql_object import MySQLObject
```

## Tests

The test uses a docker container with MySQL and a database named 'mysql_migration_test'.
    
These are the connection parameters:



```sql
CREATE database mysql_object;

USE mysql_object;

CREATE TABLE IF NOT EXISTS tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)  ENGINE=INNODB;
```


To run the tests:

    python -m unittest discover -s tests
    

## License

[MIT](LICENSE)# python-mysql-object
