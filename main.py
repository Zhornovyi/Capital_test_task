import requests
from dataclasses import dataclass
from typing import Any, Iterable
from ratelimiter import RateLimiter
from math import ceil


@dataclass
class Task:
    search_key: str
    page: int = 0


@dataclass
class TaskResult:
    task: Task
    data: Any
    next_tasks: Iterable[Task]


@dataclass
class Api:
    base_url: str
    params: dict
    endpoint: str
    task: Task = None
    task_res: TaskResult = None

    @RateLimiter(max_calls=9, period=1)
    def get(self, page, ):
        params['offset'] = page
        api_result = requests.get(self.base_url + self.endpoint, params)
        return api_result.json()

    def init_task(self, search_key, page=0):
        self.task = Task(search_key, page)

    def find_stock(self):
        while True:
            res = self.handler(self.task)
            if not res.next_tasks:
                return res.data

    @staticmethod
    def handler(task: Task):
        response = api.get(page=task.page)
        pagination = response["pagination"]
        pages_quantity = ceil(float(pagination['total']) / pagination['count'])
        index = 0
        while index < len(response['data']):
            name_value = response['data'][index]['name']
            if task.search_key not in name_value:
                del response['data'][index]
            else:
                index += 1
        data = response['data']
        if params['offset'] < pages_quantity-1:
            next_task = [Task(task.search_key, task.page+1)]
            return TaskResult(task, data, next_task)
        return TaskResult(task, data, [])


if __name__ == '__main__':
    BASE_URL = "http://api.marketstack.com/v1/"
    params = {
        'access_key': "___",
        'symbols': 'AAPL',
        'offset': 0
    }
    ENDPOINT = 'exchanges/'

    api = Api(BASE_URL, params, ENDPOINT)
    api.init_task('New York')
    result = api.find_stock()
    for i in result:
        print(i)
