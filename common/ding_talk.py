import requests
import json


def send_dingtalk_message(webhook_url, message, html_content):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": message,
            "text": f"测试报告已生成，请查收！   \n"
                    f"{html_content}"
        }
    }
    response = requests.post(url=f"{webhook_url}", headers=headers, data=json.dumps(data))
    print(response.text)
