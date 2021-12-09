import env_vars as env
import send_requests


class Notion:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {env.NOTION_SECRET_KEY}',
        'Notion-Version': '2021-08-16'
    }
    base_uri = 'https://api.notion.com/v1'
    database_id = env.NOTION_DATABASE_ID

    def __init__(self):
        pass

    @staticmethod
    def is_success(response):
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        raise Exception(f'Got {status_code}. Details: {response.text}')

    def add_page_to_database(self, properties):
        url = f'{self.base_uri}/pages'
        data = {
            'parent': {'database_id': self.database_id},
            'properties': properties
        }
        res = send_requests.post(url, headers=self.headers, data=data)
        return self.is_success(res)

    def update_page_in_database(self, page_id, properties):
        if self.get_page(page_id):
            url = f'{self.base_uri}/pages/{page_id}'
            data = {'properties': properties}
            res = send_requests.patch(url, headers=self.headers, data=data)

            return self.is_success(res)
        return

    def delete_page_in_database(self, page_id):
        if self.get_page(page_id):
            url = f'{self.base_uri}/pages/{page_id}'
            data = {'archived': True}
            res = send_requests.patch(url, headers=self.headers, data=data)
            return self.is_success(res)
        return

    def get_page(self, page_id):
        url = f'https://api.notion.com/v1/pages/{page_id}'
        res = send_requests.get(url, headers=self.headers)
        return res.status_code == 200
