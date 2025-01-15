import unittest
from common.read_yml import YamlRead
from common.general_assert import GeneralAssert
from service.base_request import BaseRequest
from service.data_delete import DataDelete
from service.data_create import DataCreate


class TestDeleteNote(unittest.TestCase):
	req = BaseRequest()
	ga = GeneralAssert()
	api_info = YamlRead()
	path = api_info.get_test_data('delete_note')['path']
	method = api_info.get_test_data('delete_note')['method']
	required = api_info.get_test_data('delete_note')['required']

	def setUp(self):
		# 清理便签数据
		delete = DataDelete()
		delete.note_delete()

	def test_major_delete_note(self):
		""" 删除便签主流程 """
		create = DataCreate()
		body = {
			'noteId': create.note_create(1)[0]['noteId']
		}
		resp = self.req.send(method=self.method, path=self.path, json=body)
		expect = {
			'responseTime': int
		}
		self.assertEqual(200, resp.status_code, msg='接口状态码校验异常')
		self.ga.http_assert(expect, resp.json())
