import glob
import os
import unittest
from common.ding_talk import send_dingtalk_message
from BeautifulReport import BeautifulReport
from datetime import datetime

DIR = os.path.dirname(os.path.abspath(__file__))
ENVIRON = 'Online'  # 'Online' -> 线上环境， 'Test' -> 测试环境

if __name__ == '__main__':
	# all 全量测试用例执行 /  smoking 冒烟测试执行  /  指定执行文件
	run_pattern = 'all'
	if run_pattern == 'all':
		pattern = 'test_*.py'
	elif run_pattern == 'smoking':
		pattern = 'test_major*.py'
	else:
		pattern = run_pattern + '.py'
	suite = unittest.TestLoader().discover('./testCase', pattern=pattern)
	result = BeautifulReport(suite)
	filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	result.report(filename=f'{filename}.html', description='测试报告', report_dir='./reports')
	# 发送钉钉消息
	file_list = glob.glob(os.path.join('./reports', '*.html'))
	if len(file_list) > 0:
		latest_file = max(file_list, key=os.path.getctime)
	else:
		latest_file = None
	webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=ca84bd151f5f54ac9400c45e4c378665e10f2185f527e6f6562266d6ffe79eef"  # 替换为实际的钉钉机器人 Webhook URL
	message = "测试报告已生成，请查收！"
	send_dingtalk_message(webhook_url, message, latest_file)
