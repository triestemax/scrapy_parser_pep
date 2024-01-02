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
        if item['status'] not in self.results:
            self.results[item['status']] = 1
        else:
            self.results[item['status']] += 1
        return item

    def close_spider(self, spider):
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
