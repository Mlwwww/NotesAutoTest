import unittest
from common.read_yml import YamlRead
from common.general_assert import GeneralAssert
from service.base_request import BaseRequest
from service.data_delete import DataDelete
from service.data_create import DataCreate


class TestHomeNotes(unittest.TestCase):
	req = BaseRequest()
	ga = GeneralAssert()
	api_info = YamlRead()
	path = api_info.get_test_data('get_home_notes')['path']
	method = api_info.get_test_data('get_home_notes')['method']
	required = api_info.get_test_data('get_home_notes')['required']

	def setUp(self):
		# 清理便签数据
		delete = DataDelete()
		delete.note_delete()
		# 新建首页便签数据
		create = DataCreate()
		create.note_create(1)

	def test_major_home_notes(self):
		""" 获取首页便签主流程 """
		resp = self.req.send(method=self.method, path=self.path)
		expect = {
			'responseTime': int,
			'webNotes': [
				{
					'noteId': str,
					'createTime': int,
					'star': 0,
					'remindTime': 0,
					'remindType': 0,
					'infoVersion': 1,
					'infoUpdateTime': int,
					'groupId': None,
					'title': str,
					'summary': str,
					'thumbnail': None,
					'contentVersion': 1,
					'contentUpdateTime': int
				}
			]
		}
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.ga.http_assert(expect, resp.json())
