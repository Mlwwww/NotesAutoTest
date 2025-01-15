import unittest
import requests
import time
from common.general_assert import GeneralAssert


class SetNoteGroupInput(unittest.TestCase):
	ga = GeneralAssert()

	def test01_major(self):
		"""新增分组接口，主流程：用户新增分组"""
		user_id = 336130547
		sid = 'V02S6-yF8N625WVPNYEnrDjKp44Ae2M00a8127ac001408f1f3'
		host = 'http://note-api.wps.cn'

		url = host + '/v3/notesvr/set/notegroup'
		headers = {
			'Cookie': f'wps_sid={sid}',
			'X-user-key': str(user_id),
			'Content-Type': 'application/json'
		}

		group_id = str(int(time.time() * 1000))
		body = {
			"groupId": group_id,
			"groupName": 'test',
			"order": 0
		}
		res = requests.post(url, headers=headers, json=body)
		self.assertEqual(200, res.status_code)

		expect = {
			"responseTime": str,
			"updateTime": int,
			"data": [
				1,
				2,
				{'1': '2'},
				str
			],
			"name": str
		}

		actual = {
			"responseTime": 19,
			"updateTime": 1733669341497,
			"data": [
				1,
				2,
				{'1': '2', '2': '2'},
				3
			]
		}
		self.ga.http_assert(expect, actual)





# self.assertEqual(200, res.status_code, msg='状态码校验失败')
# self.assertTrue('responseTime' in res.json().keys())
# self.assertTrue('updateTime' in res.json().keys())
# self.assertTrue(len(res.json().keys()) == 2)
# self.assertTrue(type(res.json()['responseTime']) == int)
# self.assertTrue(type(res.json()['updateTime']) == int)
#
# get_url = host + '/v3/notesvr/get/notegroup'
# body = {'excludeInValid': True}
# res = requests.post(get_url, headers=headers, json=body)
# self.assertTrue(len(res.json()['noteGroups']) == 1)
# self.assertTrue(res.json()['noteGroups'][0]['groupId'] == group_id)
# self.assertTrue(res.json()['noteGroups'][0]['groupName'] == 'test')
# self.assertTrue(res.json()['noteGroups'][0]['order'] == 0)
