# python mysql object

Simple Python Sqlite3 CRUD and query tool

The main usage is probably if you don't use a ORM, but query the database directly.

## Install python-mysql-object

    pip install git+https://github.com/diversen/python-sqlite-object

Or using a tag (latest):

    pip install git+https://github.com/diversen/python-sqlite-object@v0.0.1


## Usage

See [example.py](example.py) for an example.

## Tests

The following SQL creates the database and the test table:

```sql

CREATE TABLE IF NOT EXISTS tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

```


To run the tests:

    python -m unittest discover -s tests
    

## License

[MIT](LICENSE)
# python-sqlite-object
