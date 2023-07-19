from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import os


def get_db_connection():
    # Configure the database connection
    db_username = "root"
    db_password = "root"
    db_host = "localhost"
    db_port = "5432"
    db_name = "trend_impact_postgres"

    # Create the database connection URL
    db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Create the SQLAlchemy engine
    engine = create_engine(db_url)

    # Create a session factory
    Session = sessionmaker(bind=engine)

    # Return a new database session
    return Session()


# Example usage
def get_db_engine():
    # Configure the database connection
    db_username = "root"
    db_password = "root"
    db_host = "localhost"
    db_port = "5432"
    db_name = "trend_impact_postgres"

    # Create the database connection URL
    db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Create the SQLAlchemy engine
    engine = create_engine(db_url)

    return engine


def test_postgresql_connection():
    # Configure the database connection
    # the solution for problems with the connection is this:
    """
        Run docker stop trading_core_postgres to stop the container.
        Run docker rm trading_core_postgres to remove the container.
        Start the PostgreSQL container again:

    Run docker-compose up -d to start the container in detached mode.
    Wait for a few seconds to allow the container to start up and the database to be created.

    Verify the database existence:

    Run docker exec -it trading_core_postgres psql -U root -c '\l' to list the existing databases.
    Check if the "trading_core_postgres" database is present in the list.

    After following these steps, try connecting to the database using SQLAlchemy with the connection string: postgresql://root:root@localhost:5432/trading_core_postgres. The database should now exist, and the connection should be successful.

    """
    db_username = "root"
    db_password = "root"
    db_host = "localhost"
    db_port = "5432"
    db_name = "trend_impact_postgres"

    # Create the database connection URL
    db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(
        "postgresql://root:root@localhost:5432/trend_impact_postgres"
    )

    try:
        with engine.connect() as connection:
            print("Postgress connection successful")
    except Exception as e:
        print(f"Connection failed: {str(e)}")


def test_function():
    print("test")


if __name__ == "__main__":
    test_postgresql_connection()
