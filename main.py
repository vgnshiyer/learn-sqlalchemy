from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session

# -- source: https://docs.sqlalchemy.org/en/20/tutorial/engine.html --

# purpose of engine is to connect to the database
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)


# -- source: https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html --

# we use context manager to limit our use of the connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'Hello World'"))
    print(result.all())


# "commit as you go" style
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()


# begin once
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
# more concise, whole block is a transaction


with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x} y: {row.y}")


with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 6})
    for row in result:
        print(f"x: {row.x} y: {row.y}")



# using ORM
stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x} y: {row.y}")


# commit as you go
with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}]
    )
    session.commit()


# -- source: https://docs.sqlalchemy.org/en/20/tutorial/metadata.html --

