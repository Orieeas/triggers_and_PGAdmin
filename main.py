import random
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from apscheduler.schedulers.background import BackgroundScheduler


# Определение моделей
Base = declarative_base()


class DataPoint(Base):
    """DataPoint model representing a data point in the database."""
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    value = Column(Integer)


class DataPoint_onemore(Base):
    """DataPoint_onemore model representing another data point in the database."""
    __tablename__ = 'onemore'
    time = Column(DateTime, primary_key=True)
    value = Column(Integer)


class DataPointView(BaseModel):
    """DataPointView model representing the view of a data point."""
    time: datetime
    value: int


engine = create_engine('postgresql://your_username:your_password@db:5432/postgres')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Конфигурация аутентификации
security = HTTPBasic()

# Создание FastAPI приложения
app = FastAPI()


def fill_data_table():
    """Fill the 'data' table with a random data point."""
    value = random.randint(0, 10)
    id = random.randint(0, 100000)
    timestamp = datetime.now()
    session = SessionLocal()

    data_point = DataPoint(id=id, time=timestamp, value=value)
    session.add(data_point)
    session.commit()
    session.close()
    if value > 9:
        dataPoint_onemore = DataPoint_onemore(time=timestamp,value=value)
        session = SessionLocal()
        session.add(dataPoint_onemore)
        session.commit()
        session.close()


@app.on_event("startup")
def beta_data_table():
    session = SessionLocal()
    session.execute(text("""
        CREATE OR REPLACE VIEW aggregated_data_python AS
        SELECT
            date_trunc('minute', time) AS time_minute,
            COUNT(*) AS count,
            AVG(value) AS average_value
        FROM
            public."data"
        GROUP BY
            time_minute;
    """))
    session.commit()
    session.close()


scheduler = BackgroundScheduler()
scheduler.add_job(fill_data_table, 'interval', seconds=5)
scheduler.start()


# Методы API
@app.get('/data', tags=['data'])
def get_data(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Retrieve all data points from the 'data' table.

    Parameters:
        credentials: HTTPBasicCredentials
            HTTP basic authentication credentials.

    Returns:
        List[DataPointView]:
            A list of DataPointView objects representing the retrieved data points.
    """
    if not (credentials.username == 'your_username' and credentials.password == 'your_username'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    session = SessionLocal()
    data_points = session.query(DataPoint).all()
    session.close()
    return [DataPointView(time=data.time, value=data.value) for data in data_points]
