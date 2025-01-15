import unittest
from common.read_yml import YamlRead
from common.general_assert import GeneralAssert
from service.base_request import BaseRequest
import requests
from service.data_create import DataCreate
from service.data_delete import DataDelete


class TestHandleHomeNotes(unittest.TestCase):
	req = BaseRequest()
	ga = GeneralAssert()
	api_info = YamlRead()
	path = api_info.get_test_data('delete_note')['path']
	method = api_info.get_test_data('delete_note')['method']
	user_info = YamlRead()
	user_B_sid = user_info.env_config('user_B')['sid']
	user_B_id = user_info.env_config('user_B')['user_id']
	create = DataCreate()

	def setUp(self):
		# 清理便签数据
		delete = DataDelete()
		delete.note_delete()

	def test_overstep(self):
		"""越权校验"""
		body = {
			'noteId': self.create.note_create(1)[0]['noteId']
		}
		headers = {
			'Cookie': f'wps_sid={self.user_B_sid}',
			'X-user-key': '336130547',
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers, json=body)
		self.assertEqual(412, resp.status_code, msg='接口状态码校验异常')

	def test_delete_home_note(self):
		"""删除日历便签"""
		body = {
			'noteId': self.create.note_create(num=1, remind_time=1211)[0]['noteId']
		}
		resp = self.req.send(method=self.method, path=self.path, json=body)
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')

	def test_delete_group_note(self):
		"""删除分组便签"""
		body = {
			'noteId': self.create.note_create(num=1, group_id=1211)[0]['noteId']
		}
		resp = self.req.send(method=self.method, path=self.path, json=body)
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')

	def test_repeat_delete_note(self):
		"""重复删除noteId"""
		body = {
			'noteId': self.create.note_create(1)[0]['noteId']
		}
		self.req.send(method=self.method, path=self.path, json=body)
		resp = self.req.send(method=self.method, path=self.path, json=body)
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')