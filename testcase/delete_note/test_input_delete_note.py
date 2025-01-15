import unittest
from common.read_yml import YamlRead
from common.general_assert import GeneralAssert
from service.base_request import BaseRequest
import requests


class TestHomeNotes(unittest.TestCase):
	req = BaseRequest()
	ga = GeneralAssert()
	api_info = YamlRead()
	path = api_info.get_test_data('get_home_notes')['path']
	method = api_info.get_test_data('get_home_notes')['method']

	def test_required_user01(self):
		""" 校验获取首页便签必填项user_id为空 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/''/home/startindex/0/rows/50/notes')
		self.assertEqual(404, resp.status_code, msg='接口状态码校验异常')

	def test_required_user02(self):
		""" 校验获取首页便签必填项user_id缺失 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/home/startindex/0/rows/50/notes')
		self.assertEqual(404, resp.status_code, msg='接口状态码校验异常')

	def test_required_user03(self):
		""" 校验获取首页便签必填项user_id为字符串 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/"336130547"/home/startindex/0/rows/50/notes')
		self.assertEqual(500, resp.status_code, msg='接口状态码校验异常')

	def test_required_startindex01(self):
		""" 校验获取首页便签必填项startindex为空 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/''/rows/50/notes')
		self.assertEqual(404, resp.status_code, msg='接口状态码校验异常')

	def test_required_startindex02(self):
		""" 校验获取首页便签必填项startindex缺失 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/rows/50/notes')
		self.assertEqual(404, resp.status_code, msg='接口状态码校验异常')

	def test_required_startindex03(self):
		""" 校验获取首页便签必填项startindex为字符串 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/"0"/rows/50/notes')
		self.assertEqual(500, resp.status_code, msg='接口状态码校验异常')

	def test_required_rows01(self):
		""" 校验获取首页便签必填项rows为空 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/0/rows/''/notes')
		self.assertEqual(404, resp.status_code, msg='接口状态码校验异常')

	def test_required_rows02(self):
		""" 校验获取首页便签必填项rows缺失 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/rows/notes')
		self.assertEqual(404, resp.status_code, msg='接口状态码校验异常')

	def test_required_rows03(self):
		""" 校验获取首页便签必填项rows为字符串 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/0/rows/"50"/notes')
		self.assertEqual(500, resp.status_code, msg='接口状态码校验异常')

	def test_cookie01(self):
		""" 校验获取首页便签header中cookie的sid缺失"""
		headers = {
			'Cookie': '',
			'X-user-key': str(self.req.user_id),
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')

	def test_cookie02(self):
		""" 校验获取首页便签header中cookie中sid失效"""
		headers = {
			'Cookie': 'wps_sid=123asdas2',
			'X-user-key': str(self.req.user_id),
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')

	def test_X_user_key01(self):
		""" 校验获取首页便签header中cookie的X-user-key缺失"""
		headers = {
			'Cookie': '',
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')

	def test_X_user_key02(self):
		""" 校验获取首页便签header中cookie的X-user-key错误"""
		headers = {
			'Cookie': '',
			'X-user-key': '1111',
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')