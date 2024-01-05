import csv
import datetime as dt
import os


from pathlib import Path


BASE_DIR = Path(__file__).parent.parent / 'results'
DATE = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


class PepParsePipeline:
    def open_spider(self, spider):
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        self.results = {}

    def process_item(self, item, spider):
        self.results[item['status']] = self.results.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        file_name = f'status_summary_{DATE}.csv'
        with open(
            os.path.join(BASE_DIR, file_name),
            mode='w',
            encoding='utf-8'
        ) as file:
            file.write('Статус,Количество\n')
            writer = csv.writer(file)
            writer.writerows(self.results.items())
            file.write(f'Total,{sum(self.results.values())}\n')
