import time
import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey, Float, Integer, BigInteger, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from lgbsttracker.entities import LightSensor as LightSensorEntity

from lgbsttracker.store.db.base_sql_model import Base


class SqlLightSensor(Base):
    __tablename__ = "light_sensor"

    light_sensor_id = Column(Integer)  # autoincrement
    name = Column(String(32))
    creation_time = Column(DateTime, default=str(datetime.datetime.now()))
    value = Column(Float, nullable=True, default=None)
    last_updated_time = Column(DateTime, nullable=True, default=None)

    __table_args__ = (PrimaryKeyConstraint("light_sensor_id", name="light_sensor_pk"),)

    # entity mappers
    def to_entity(self):
        return LightSensorEntity(self.light_sensor_id, self.name, self.value, self.creation_time, self.last_updated_time)
