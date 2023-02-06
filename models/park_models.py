from datetime import timedelta, timezone, datetime
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, INT, DateTime, Boolean

from lib.config import settings


engine = create_engine(
    "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}".format(
        user=settings.dbuser,
        passwd=quote_plus(settings.passwd),
        host=settings.host,
        port=settings.port,
        database=settings.database,
    )
)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)


class ParkHistory(Base):
    __tablename__ = 'park_history'

    id = Column(INT, primary_key=True, autoincrement=True)
    plate = Column(String(255), index=True)
    create_time = Column(DateTime, server_default=func.now())
    deleted = Column(Boolean, default=False)

    @staticmethod
    def add_car(plate: str) -> bool:
        with DBSession() as session:
            history = session.query(func.count(ParkHistory.id)).filter(
                ParkHistory.plate == plate
            ).filter(
                ParkHistory.deleted.isnot(True)
            ).one()
            count = history[0] if history else 0
            if count:
                return False
            session.add(ParkHistory(plate=plate))
            session.commit()
            return True

    @staticmethod
    def calc_car(plate: str) -> datetime:
        with DBSession() as session:
            history = session.query(ParkHistory).filter(
                ParkHistory.plate == plate
            ).filter(
                ParkHistory.deleted.isnot(True)
            ).order_by(ParkHistory.create_time.desc()).first()
            if not history:
                return None
            return history.create_time.astimezone(tz=timezone.utc)

    @staticmethod
    def del_car(plate: str) -> None:
        with DBSession() as session:
            session.query(ParkHistory).filter(
                ParkHistory.plate == plate
            ).filter(
                ParkHistory.deleted.isnot(True)
            ).update({"deleted": True})
            session.commit()

    @staticmethod
    def count_car() -> int:
        with DBSession() as session:
            history = session.query(
                func.count(ParkHistory.id)
            ).filter(
                ParkHistory.deleted.isnot(True)
            ).one()
            return history[0] if history else 0


Base.metadata.create_all(engine)
