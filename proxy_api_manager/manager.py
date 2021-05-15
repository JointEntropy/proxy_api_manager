from .proxy6api import Proxy6API


PROXY6 = 'PROXY6'
PROXY_API_CHOICE = {
    PROXY6: Proxy6API
}


class ProxyManager:
    def __init__(self, proxies_config):
        api_class = PROXY_API_CHOICE[proxies_config['api_class']]
        api_params = proxies_config.get('api_settings', {})
        self.api = api_class(**api_params)

    def get_proxies_list(self):
        return list(self.api.get_ipv4_proxies())

    @staticmethod
    def list_aval_apis():
        return list(PROXY_API_CHOICE.keys())


if __name__ == '__main__':
    import json
    import os

    print(ProxyManager.list_aval_apis())
    CONFIG_PATH = os.environ['CONFIG_PATH']
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    manager = ProxyManager(config['proxies'])
    print(list(manager.get_proxies_list()))

