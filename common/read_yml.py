from main import DIR, ENVIRON
import yaml


class YamlRead:
    @staticmethod
    def env_config(user):
        """环境变量的读取方式"""
        with open(file=f'{DIR}/config/env_config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)[f'{ENVIRON}'][f'{user}']

    @staticmethod
    def get_test_data(name):
        with open(file=f'{DIR}/config/api_config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)[f'{name}']


if __name__ == '__main__':
    YR = YamlRead
    # print(YR.env_config('user_A'))
    print(YR.get_test_data('get_home_notes'))