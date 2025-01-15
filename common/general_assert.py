import unittest


class GeneralAssert(unittest.TestCase):
	"""
	各种通讯协议的通用断言方法，包含的协议包括：
	http协议： http_assert();
	rpc协议： rpc_assert()
	"""

	def http_assert(self, expect, actual):
		"""
		http协议的通用断言方法
		:param expect: 接口返回的预期值，类型是dict or list
		:param actual: 接口实际返回值，类型是dict or list
		:return:
		"""
		if isinstance(actual, dict):
			with self.subTest(msg='校验字典key的长度'):
				self.assertEqual(len(expect.keys()), len(actual.keys()), msg=f'预期返回的key {list(expect.keys())} 和实际返回的key {list(actual.keys())}的长度不一致')
			for k, v in expect.items():
				with self.subTest(msg=f"检查键 {k} 是否存在于实际返回字典中"):
					self.assertIn(k, actual.keys(), msg=f'实际返回的键中{actual.keys()}缺少{k}')
				if isinstance(v, type):
					with self.subTest(msg=f"检查键 {k} 对应值的数据类型是否符合预期"):
						self.assertEqual(v, type(actual[k]), msg=f'{actual[k]}返回的数据类型与预期{v}不一致')
				elif isinstance(v, list):
					with self.subTest(msg=f"检查键 {k} 对应列表长度是否符合预期"):
						self.assertEqual(len(v), len(actual[k]), msg=f'{actual[k]}的列表长度与预期{v}的长度不一致')
					for i in range(len(v)):
						if isinstance(v[i], type):
							with self.subTest(msg=f"检查键 {k} 列表下第 {i + 1} 个元素类型是否符合预期"):
								self.assertEqual(v[i], type(actual[k][i]),
												 msg=f'{k}列表下的第{i + 1}个元素类型与实际返回的类型不一致')
						elif isinstance(v[i], dict):
							self.http_assert(v[i], actual[k][i])
						else:
							with self.subTest(msg=f"检查键 {k} 列表下第 {i + 1} 个元素值是否符合预期"):
								self.assertEqual(v[i], actual[k][i],
												 msg=f'{k}列表下的第{i + 1}个元素值与实际返回的值不一致')
				else:
					with self.subTest(msg=f"检查键 {actual[k]} 元素值是否符合预期"):
						self.assertEqual(v, actual[k], msg=f'{actual[k]}字段不一致')
		else:
			if isinstance(actual, list):
				with self.subTest(msg="比较列表长度是否一致"):
					self.assertEqual(len(expect), len(actual), msg=f'{expect}的列表长度与预期{actual}的长度不一致')
				for i in range(len(expect)):
					if isinstance(expect[i], type):
						with self.subTest(msg=f"检查列表下第 {i + 1} 个元素类型是否符合预期"):
							self.assertEqual(expect[i], type(actual[i]),
											 msg=f'列表下的第{i + 1}个元素类型与实际返回的类型不一致')
					elif isinstance(expect[i], dict):
						self.http_assert(expect[i], actual[i])
					elif isinstance(expect[i], list):
						self.http_assert(expect[i], actual[i])
					else:
						with self.subTest(msg=f"检查列表下第 {i + 1} 个元素值是否符合预期"):
							self.assertEqual(expect[i], actual[i], msg=f'列表下的第{i + 1}个元素值与实际返回的值不一致')

	def rpc_assert(self, expect, actual):
		"""

		:param expect:
		:param actual:
		:return:
		"""
		pass
