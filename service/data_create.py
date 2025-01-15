import time
from service.base_request import BaseRequest


class DataCreate(BaseRequest):
	"""创建测试数据"""

	def note_create(self, num, group_id=None, remind_time=None):
		"""通用的便签新建方法"""
		note_lists = []
		for i in range(num):
			note_id = str(int(time.time() * 1000))

			if remind_time:  # 日历便签
				body = {
					"noteId": note_id,
					"remindTime": remind_time,
					"remindType": 0,
					'star': 0
				}

			elif group_id:  # 分组便签
				body = {
					"noteId": note_id,
					"groupId": group_id,
					'star': 0
				}

			else:  # 首页便签
				body = {
					"noteId": note_id,
					'star': 0
				}
			self.send(method='POST', path='/v3/notesvr/set/noteinfo', json=body)  # 创建便签

			body = {
				"noteId": note_id,
				"title": 'test',
				"summary": 'test',
				"body": 'test',
				"localContentVersion": 1,
				"BodyType": 0
			}
			self.send(method='POST', path='/v3/notesvr/set/notecontent', json=body)  # 添加内容
			note_lists.append(body)
		return note_lists


if __name__ == '__main__':
	DC = DataCreate()
	print(DC.note_create(num=1, group_id='d24f01a3b8492fed6aadca03c3e49277'))
