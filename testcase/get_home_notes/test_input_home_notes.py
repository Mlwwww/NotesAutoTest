import unittest
from common.read_yml import YamlRead
from common.general_assert import GeneralAssert
from service.base_request import BaseRequest
import requests
from service.data_delete import DataDelete
from service.data_create import DataCreate


class TestHomeNotes(unittest.TestCase):
	req = BaseRequest()
	ga = GeneralAssert()
	api_info = YamlRead()
	path = api_info.get_test_data('delete_note')['path']
	method = api_info.get_test_data('delete_note')['method']
	required = api_info.get_test_data('delete_note')['required']
	create = DataCreate()

	def setUp(self):
		# 清理便签数据
		delete = DataDelete()
		delete.note_delete()

	def test_required_noteId01(self):
		"""校验必填项noteId缺失"""
		body = {
		}
		resp = self.req.send(method=self.method, path=self.path, json=body)
		self.assertEqual(500, resp.status_code, msg='接口状态码校验异常')


	def test_required_noteId02(self):
		"""校验必填项noteId传None"""
		body = {
			'noteId': None
		}
		resp = self.req.send(method=self.method, path=self.path, json=body)
		self.assertEqual(500, resp.status_code, msg='接口状态码校验异常')

	def test_required_noteId03(self):
		"""校验必填项noteId传特殊字符"""
		body = {
			"noteId": "@#$!!123.zz"
		}
		resp = self.req.send(method=self.method, path=self.path, json=body)
		self.assertEqual(500, resp.status_code, msg='接口状态码校验异常')

	def test_required_noteId04(self):
		"""校验必填项noteId传空"""
		body = {
			"noteId": ""
		}
		resp = self.req.send(method=self.method, path=self.path, json=body)
		self.assertEqual(500, resp.status_code, msg='接口状态码校验异常')

	def test_cookie01_delete_note(self):
		""" 删除便签header中cookie的sid缺失"""
		body = {
			'noteId': self.create.note_create(1)[0]['noteId']
		}
		headers = {
			'Cookie': '',
			'X-user-key': str(self.req.user_id),
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers, json=body)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')

	def test_cookie02_delete_note(self):
		""" 删除便签header中cookie中sid失效"""
		headers = {
			'Cookie': 'wps_sid=123asdas2',
			'X-user-key': str(self.req.user_id),
			'Content-Type': 'application/json'
		}
		body = {
			'noteId': self.create.note_create(1)[0]['noteId']
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers, json=body)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')

	def test_X_user_key01(self):
		""" 校验获取首页便签header中cookie的X-user-key缺失"""
		body = {
			'noteId': self.create.note_create(1)[0]['noteId']
		}
		headers = {
			'Cookie': '',
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers, json=body)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')

	def test_X_user_key02(self):
		""" 校验获取首页便签header中cookie的X-user-key错误"""
		body = {
			'noteId': self.create.note_create(1)[0]['noteId']
		}
		headers = {
			'Cookie': '',
			'X-user-key': '1111',
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers, json=body)
		self.assertEqual(401, resp.status_code, msg='接口状态码校验异常')
