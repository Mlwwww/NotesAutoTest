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
	path = api_info.get_test_data('get_home_notes')['path']
	method = api_info.get_test_data('get_home_notes')['method']
	user_info = YamlRead()
	user_B_sid = user_info.env_config('user_B')['sid']
	user_B_id = user_info.env_config('user_B')['user_id']

	def setUp(self):
		# 清理便签数据
		delete = DataDelete()
		delete.note_delete()

	def test_overstep(self):
		""" 越权校验 """
		# 新建首页便签数据
		create = DataCreate()
		create.note_create(2)
		headers = {
			'Cookie': f'wps_sid={self.user_B_sid}',
			'X-user-key': '336130547',
			'Content-Type': 'application/json'
		}
		resp = requests.request(method=self.method, url=self.req.host + self.path, headers=headers)
		self.assertEqual(412, resp.status_code, msg='接口状态码校验异常')

	def test_value_constraints_startindex(self):
		""" 校验获取首页便签startindex=1 """
		# 新建首页便签数据
		create = DataCreate()
		create.note_create(1)
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/1/rows/50/notes')
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')

	def test_value_constraints_rows(self):
		""" 校验获取首页便签rows=1 """
		# 新建首页便签数据
		create = DataCreate()
		create.note_create(2)
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/1/rows/50/notes')
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.assertEqual(1, len(resp.json()['webNotes']), msg='获取的便签数量不对')

	def test_amount0_home_notes(self):
		""" 获取0个首页便签 """
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/0/rows/50/notes')
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.assertEqual(0, len(resp.json()['webNotes']), msg='获取的便签数量不对')

	def test_amount1_home_notes(self):
		""" 获取1个首页便签 """
		create = DataCreate()
		create.note_create(1)
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/0/rows/50/notes')
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.assertEqual(1, len(resp.json()['webNotes']), msg='获取的便签数量不对')

	def test_amount2_home_notes(self):
		""" 获取2个首页便签 """
		create = DataCreate()
		create.note_create(2)
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/0/rows/50/notes')
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.assertEqual(2, len(resp.json()['webNotes']), msg='获取的便签数量不对')

	def test_other_type_group_notes(self):
		""" 校验是否获取分组便签 """
		create = DataCreate()
		create.note_create(num=1, group_id=1211)
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/0/rows/50/notes')
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.assertEqual(0, len(resp.json()['webNotes']), msg='获取的便签数量不对')

	def test_other_type_calendar_notes(self):
		""" 校验是否获取日历便签 """
		create = DataCreate()
		create.note_create(num=1, remind_time=1211)
		resp = self.req.send(method=self.method, path='/v3/notesvr/user/336130547/home/startindex/0/rows/50/notes')
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.assertEqual(0, len(resp.json()['webNotes']), msg='获取的便签数量不对')
