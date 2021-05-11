import json
from datetime import datetime

import requests

from dlc_oracle_bot.logging_utility import log
from dlc_oracle_bot.oracle.schema_validation import event_schema


class OracleClient(object):
    def __init__(self, host: str, port: int):
        # noinspection HttpUrlsUsage
        self.url = f'http://{host}:{port}'
        self.headers = {'Content-Type': 'application/json'}

    def query_oracle(self, query_data: dict):
        request_data = {
            'jsonrpc': '1.0',
            'id': 'curltest'
        }
        request_data.update(query_data)
        log.debug('query_oracle', request_data=request_data)
        response = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps(request_data)
        )
        response.raise_for_status()
        response_data = json.loads(response.text)
        log.debug('query_oracle', response_data=response_data)
        if response_data['error'] is not None:
            raise Exception('Oracle client error')
        return response_data['result']

    def get_public_key(self):
        response = self.query_oracle({'method': 'getpublickey'})
        return response

    def create_event(
            self,
            label: str,
            maturation: datetime,
            minimum: int,
            maximum: int,
            unit: str,
            precision: int
    ):
        create_data = {
            'method': 'createnumericevent',
            'params': [
                label,
                maturation.isoformat(),
                minimum,
                maximum,
                unit,
                precision
            ]
        }
        response = self.query_oracle(create_data)
        return response

    def list_events(self):
        response = self.query_oracle({'method': 'listevents'})
        return response

    def get_event(self, label: str):
        get_event_data = {
            'method': 'getevent',
            'params': [
                label
            ]
        }
        response = self.query_oracle(get_event_data)
        if response is None:
            return None
        validated_response = event_schema.load(response)
        return validated_response

    def sign_event(self, label: str, value: int):
        sign_data = {
            'method': 'signdigits',
            'params': [
                label,
                value
            ]
        }
        response = self.query_oracle(sign_data)
        return response

    def get_signatures(self, label: str):
        get_signatures = {
            'method': 'getsignatures',
            'params': [
                label
            ]
        }
        response = self.query_oracle(get_signatures)
        return response


if __name__ == '__main__':
    import os

    from dotenv import load_dotenv

    load_dotenv()
    client = OracleClient(host=os.environ['ORACLE_SERVER_HOST'],
                          port=int(os.environ['ORACLE_SERVER_PORT']))
