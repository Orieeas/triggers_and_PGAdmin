import pytest
import httpx
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


@pytest.fixture
def test_db():
    engine = create_engine('postgresql://your_username:your_password@localhost:5432/postgres')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_get_employees_with_invalid_email(test_db):
    url = 'http://localhost:8000/data'
    credentials = ('your_username', 'your_password')

    with httpx.Client() as client:
        response = client.get(url, auth=credentials)
    assert response.status_code == 401


def test_get_employees_with_valid_email(test_db):
    url = 'http://localhost:8000/data'
    credentials = ('your_username', 'your_password')

    with httpx.Client() as client:
        response = client.get(url, auth=credentials)
    assert response.status_code == 401
