import json
import requests
from common.log_until import logger
from common.read_yml import YamlRead


class BaseRequest:
	def __init__(self):
		get_config = YamlRead
		self.host = get_config.env_config('user_A')['host']
		self.sid = get_config.env_config('user_A')['sid']
		self.user_id = get_config.env_config('user_A')['user_id']
		self.headers = {
			'Cookie': f'wps_sid={self.sid}',
			'X-user-key': str(self.user_id),
			'Content-Type': 'application/json'
		}

	def send(self, method, path, **kwargs):
		num = 3
		while num:
			num -= 1
			try:
				res = requests.request(method=method, url=self.host + path, headers=self.headers, **kwargs)
				logger.info(f'请求地址：{self.host + path}')
				logger.info(f'请求方法：{method}')
				logger.info(f'请求参数{json.dumps(kwargs, indent=2, ensure_ascii=False)}')
				logger.info(f'Response{json.dumps(res.json(), indent=2, ensure_ascii=False)}')
				return res
			except requests.RequestException as e:
				logger.info(f"请求失败: {e}")
		return None



