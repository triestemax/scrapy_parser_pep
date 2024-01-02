import datetime as dt
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent / 'results'
DATE = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


Base = declarative_base()


class Pep(Base):
    __tablename__ = 'pep'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(200))
    status = Column(String(50))


class PepParsePipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///results/sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)
        self.results = {}

    def process_item(self, item, spider):
        if item['status'] not in self.results:
            self.results[item['status']] = 1
        else:
            self.results[item['status']] += 1
        pep = Pep(
            number=item['number'], name=item['name'], status=item['status']
        )
        self.session.add(pep)
        self.session.commit()
        return item

    def close_spider(self, spider):
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        file_name = f'status_summary_{DATE}.csv'
        with open(
            os.path.join(BASE_DIR, file_name),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write('Статус,Количество\n')
            for key, value in self.results.items():
                file.write(f'{key},{value}\n')
            file.write(f'Total,{sum(self.results.values())}')
        self.session.close()
