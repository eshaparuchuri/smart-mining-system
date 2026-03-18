from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///data.db")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer)
    temperature = Column(Float)
    vibration = Column(Float)
    load = Column(Float)
    pressure = Column(Float)
    timestamp = Column(String)

Base.metadata.create_all(bind=engine)