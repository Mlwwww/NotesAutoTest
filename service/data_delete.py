from service.base_request import BaseRequest


class DataDelete(BaseRequest):
	"""删除便签数据"""

	def note_delete(self):
		""""""
		note_ids = []
		group_id = []
		# step1 获取首页便签，提取noteId
		resp = self.send(method='GET', path=f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/50/notes')
		for item in resp.json()['webNotes']:
			note_ids.append(item['noteId'])

		# step2 获取日历便签，提取noteId
		calendar_note_body = {
			'startindex': 0,
			'rows': 300,
			'remindStartTime': 1732982400000,
			'remindEndTime': 1735660800000
		}
		resp = self.send(method='POST', path='/v3/notesvr/web/getnotes/remind', json=calendar_note_body)
		for item in resp.json()['webNotes']:
			note_ids.append(item['noteId'])

		# step3 获取分组便签，提取noteId
		group_id_body = {
			'excludeInValid': True,
			'lastRequestTime': 0
		}
		resp = self.send(method='POST', path='/v3/notesvr/get/notegroup', json=group_id_body)  # 获取group_id
		for item in resp.json()['noteGroups']:
			group_id.append(item['groupId'])

		for i in group_id:
			group_note_body = {
				'groupId': i,
				'rows': 50,
				'startIndex': 0
			}
			resp = self.send(method='POST', path='/notesvr/web/getnotes/group', json=group_note_body)  # 获取分组便签的note_id
			for item in resp.json()['webNotes']:
				note_ids.append(item['noteId'])

		# step4 循环noteId，尽量循环删除
		for i in note_ids:
			delete_body = {
				'noteId': i
			}
			self.send(method='POST', path='/notesvr/delete', json=delete_body)

		# step5 清空回收站
		recyclebin_body = {
			'noteIds': ["-1"]
		}
		self.send(method='POST', path='/notesvr/cleanrecyclebin', json=recyclebin_body)


if __name__ == '__main__':
	DD = DataDelete()
	print(DD.note_delete())
