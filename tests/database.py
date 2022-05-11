from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from alembic import command

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Sachin@123@localhost/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)  # used to create tables

# Dependency
#def override_get_db():
#    db = TestingSessionLocal() # connecting to the DBs, calling this func everytime when we get api request
#    try:
#        yield db
#    finally:
#        db.close()

#app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal() # connecting to the DBs, calling this func everytime when we get api request
    try:
        yield db #db object
    finally:
        db.close()

#client = TestClient(app)

@pytest.fixture()
def client(session):
    # run our code before we return our TestClient
    #Base.metadata.create_all(bind=engine)  # used to create tables using sqlalchemy
    #command.upgrade("head") # using alembic
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run our code after we return our TestClient
    #Base.metadata.drop_all(bind=engine)  # used to drop tables using sqlalchemy
    #command.downgrade("base") # using alembic
