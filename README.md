# python mysql object

Simple Python MySQL CRUD and query tool

The main usage is probably if you don't use a ORM, but query the MySQL database directly using `mysql.connector`.

## Install python-mysql-object

    pip install git+https://github.com/diversen/python-mysql-object

Or using a tag (latest):

    pip install git+https://github.com/diversen/python-mysql-object@v0.0.5


## Usage

See [example.py](example.py) for an example.

## Tests

The test uses a docker container with MySQL and a database named 'mysql_object'.

No mocking.

These are [the connection parameters](tests/settings.py):

The following SQL creates the database and the test table:

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

[MIT](LICENSE)
