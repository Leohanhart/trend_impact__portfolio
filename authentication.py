# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:08:35 2023

@author: Gebruiker

USERADMIN   : LEODEADMIN
PASSWORD    : QWERTY12345...LEOISADMIN  

"""

from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import jwt
from database_querys_main import database_querys
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    func,
    delete,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func
from sqlalchemy import or_
from sqlalchemy import desc
from contextlib import contextmanager
import constants
import json

app = FastAPI()

# JWT configuration
SECRET_KEY = "WeAreTotallyLocoJustLikeTheCobos"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db_path = constants.SQLALCHEMY_DATABASE_URI_layer_zero
engine = create_engine(db_path, echo=False)
Session = sessionmaker(bind=engine)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    endpoint = Column(String)
    values = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())


# Check if the table already exists
# Create an inspector to inspect the database
inspector = inspect(engine)

# Check if the table already exists
table_exists = inspector.has_table("users")


# Create the table if it does not exist
if not table_exists:
    Base.metadata.create_all(engine)

# Check if the table already exists
table_exists = inspector.has_table("user_activity")

if not table_exists:
    Base.metadata.create_all(engine)


def get_user_activity_data(
    search_endpoint: str = None,
    search_user: str = None,
    page: int = 1,
    page_size: int = 100,
):
    with get_db() as db:
        # Query the user_activity table based on the search criteria
        query = db.query(UserActivity)
        if search_endpoint:
            query = query.filter(UserActivity.endpoint == search_endpoint)
        if search_user:
            query = query.filter(UserActivity.user == search_user)

        # Determine the total number of rows matching the search criteria
        total_rows = query.count()

        # Apply pagination to the query
        query = (
            query.order_by(desc(UserActivity.timestamp))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        # Retrieve the data
        results = query.all()

        # Convert the data to a list of dictionaries
        data = []
        for result in results:
            data.append(
                {
                    "id": result.id,
                    "user": result.user,
                    "endpoint": result.endpoint,
                    "values": result.values,
                    "timestamp": result.timestamp,
                }
            )

        # Create a dictionary with the pagination information
        pagination = {
            "page": page,
            "page_size": page_size,
            "total_rows": total_rows,
        }

        # Create a dictionary to hold the final result
        response = {"data": data, "pagination": pagination}

        # Convert the response to JSON format
        json_response = json.dumps(response)

        # Return the JSON response
        return json_response


def log_user_activity(username: str, endpoint: str, values: str):

    if endpoint == "" or endpoint is None:
        return
    # Get the database session using the context manager
    with get_db() as db:
        activity = UserActivity(
            user=username,
            endpoint=endpoint,
            values=values,
            timestamp=datetime.now(),
        )
        db.add(activity)
        db.commit()

        # Calculate the cutoff timestamp
        cutoff_timestamp = datetime.now() - timedelta(days=1.5 * 365)

        # Construct the DELETE statement
        delete_statement = delete(UserActivity).where(
            UserActivity.timestamp < cutoff_timestamp
        )

        # Execute the DELETE statement
        with engine.begin() as connection:
            connection.execute(delete_statement)

        # Commit the changes
        session.commit()


def get_db():
    db = Session()
    return db


def check_user(username: str, password: str) -> bool:
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        if user and user.password == password:
            return user.role
        return None


def add_user(username: str, password: str, role: str):
    with get_db() as db:
        user = User(username=username, password=password, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)


def change_password(username: str, new_password: str):
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise Exception("User not found")
        user.password = new_password
        db.commit()


def delete_user(username: str):
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise Exception("User not found")
        db.delete(user)
        db.commit()


# Generate JWT token with user roles
def generate_token(username: str, roles: list) -> str:
    expires = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"username": username, "roles": roles, "exp": expires}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# Verify JWT token and extract user roles
def verify_token(
    token: str,
    expected_roles: list = ["USER", "ADMIN"],
    endpoint: str = "",
    values: str = "",
) -> tuple:
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        roles = payload.get("roles")
        if username:
            if roles in expected_roles:

                log_user_activity(username, endpoint, values)

                return username, roles
            else:
                raise HTTPException(status_code=401, detail="Unauthorized")

        if roles is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except jwt.ExpiredSignatureError:
        pass
    except jwt.DecodeError:
        pass

    raise HTTPException(status_code=401, detail="Unauthorized")

    return None, None


def login_user(username, password):
    role = check_user(username, password)

    if role is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        token = generate_token(username, role)
        return token


def protected_add_user(token, username_new, password_new, user_role_new):
    username, role = verify_token(token, ["ADMIN"])
    if role is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role == "ADMIN":
        add_user(username_new, password_new, user_role_new)


def protected_change_password(token, username_new, password_new):
    username, role = verify_token(token, "ADMIN")
    if role is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role == "ADMIN":
        change_password(username_new, password_new)


def protected_delete_user(token, username_new):
    username, role = verify_token(token, "ADMIN")
    if role is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role == "ADMIN":
        delete_user()(username_new)


# Generate JWT token endpoint
def generate_token_endpoint(username: str, roles: list):
    token = generate_token(username, roles)
    return {"access_token": token}


# Verify JWT token endpoint
def verify_token_endpoint(token: str):
    username, roles = verify_token(token)
    if username is None:
        return {"valid": False}
    return {"valid": True, "username": username, "roles": roles}


if __name__ == "__main__":

    try:
        x = get_user_activity_data(search_user="LEODEADMIN")
        # add_user("LEODEADMIN", "QWERTY12345...LEOISADMIN", "ADMIN")
        print("est", x)

    except Exception as e:

        raise Exception("Database could not be created", e)
