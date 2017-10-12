from scrapy_sqlitem import SqlItem
from sqlalchemy import Column, String, Text, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ListingModel(Base):
    __tablename__ = 'listing'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    price = Column(Float)
    scraped_at = Column(DateTime)
    text = Column(Text)


class ListingItem(SqlItem):
    sqlmodel = ListingModel
