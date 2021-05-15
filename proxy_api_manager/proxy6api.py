import requests


class Proxy6API:
    """
    https://proxy6.net/en/developers

    Example:
    ```
    API_KEY = '<YOUR_API_KEY>'
    api = Proxy6API(API_KEY=API_KEY)
    print(list(api.get_proxies(filter_entry=api.is_ipv4)))
    ```
    """
    base_url = 'https://proxy6.net'

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_ipv4_proxies(self):
        return self.get_proxies(filter_entry=self.is_ipv4)

    def get_ipv6_proxies(self):
        return self.get_proxies(filter_entry=self.is_ipv6)

    def get_proxies(self, filter_entry=None):
        method = 'getproxy'
        url = f'{self.base_url}/api/{self.API_KEY}/{method}'
        response = requests.get(url,
                                params=[
                                    ('state', 'active'),
                                    ('nokey', None)
                                ]
        )
        assert response.status_code == 200, f'Invalid response from {self.base_url}'

        proxies_json = response.json()
        for proxy_info_entry in proxies_json['list'].values():
            if not filter_entry(proxy_info_entry):
                continue
            yield self.get_ip_string(proxy_info_entry)

    @staticmethod
    def is_ipv4(proxy_info_entry):
        if proxy_info_entry['version'] == '4':
            return True
        return False

    @staticmethod
    def is_ipv6(proxy_info_entry):
        if proxy_info_entry['version'] == '6':
            return True
        return False

    @staticmethod
    def get_ip_string(r):
        # 'https://{name}:{pass}@213.226.78.187:8000'
        ip_string = 'https://{user}:{password}@{host}:{port}'.format(
            user=r['user'],
            password=r['pass'],
            host=r['host'],
            port=r['port']
        )
        return ip_string


if __name__ == '__main__':
    import json
    import os
    CONFIG_PATH = os.environ['CONFIG_PATH']
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    api = Proxy6API(**config['proxies']['api_settings'])
    print(list(api.get_proxies(filter_entry=api.is_ipv4)))
