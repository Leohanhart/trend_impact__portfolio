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
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect

import constants

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


# Check if the table already exists
# Create an inspector to inspect the database
inspector = inspect(engine)

# Check if the table already exists
table_exists = inspector.has_table("users")


# Create the table if it does not exist
if not table_exists:
    Base.metadata.create_all(engine)


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
    token: str, expected_roles: list = ["USER", "ADMIN"]
) -> tuple:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        roles = payload.get("roles")
        if username:

            if roles in expected_roles:
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
    username, role = verify_token(token)
    if role is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role == "ADMIN":
        add_user(username_new, password_new, user_role_new)


def protected_change_password(token, username_new, password_new):
    username, role = verify_token(token)
    if role is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role == "ADMIN":
        change_password(username_new, password_new)


def protected_delete_user(token, username_new):
    username, role = verify_token(token)
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
        protected_add_user(
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkxFT0RFQURNSU4iLCJyb2xlcyI6IkFETUlOIiwiZXhwIjoxNjg4MDcwNzY2fQ.Xx54uYHp9qTX6QffPgXew2WhwulAj70mv8kS5BAL1TA",
            "KWEE",
            "UTRECHT123OPENICT",
            "SIENTIST",
        )
        # add_user("LEODEADMIN", "QWERTY12345...LEOISADMIN", "ADMIN")
        print("est")

    except Exception as e:

        raise Exception("Database could not be created", e)
