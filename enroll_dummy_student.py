"""
⚠️Warning: The target server for this operation must be a PowerSchool test server instance. This code assumes no responsibility for any adverse outcomes.
⚠️警告：此操作目标服务器必须是一个 PowerSchool 测试服务器实例，本代码不对任何负面结果承担任何责任
"""

import os
import json
import colorama
from faker import Faker
from colorama import Fore
from dotenv import load_dotenv
from powerschool_adapter.powerschool import PowerSchool

load_dotenv()
fake = Faker()
colorama.init(autoreset=True)

if (os.getenv('POWERSCHOOL_SERVER_ADDRESS') is None or
		os.getenv('POWERSCHOOL_CLIENT_ID') is None or
		os.getenv('POWERSCHOOL_CLIENT_SECRET') is None):
	print("PowerSchool environment variables were not set.")
	exit()

POWERSCHOOL_SERVER_ADDRESS = os.getenv("POWERSCHOOL_SERVER_ADDRESS")
POWERSCHOOL_CLIENT_ID = os.getenv("POWERSCHOOL_CLIENT_ID")
POWERSCHOOL_CLIENT_SECRET = os.getenv("POWERSCHOOL_CLIENT_SECRET")

DUMMY_SCHOOL_NUMBER = 5

powerschool = PowerSchool(
	server_address=POWERSCHOOL_SERVER_ADDRESS,
	client_id=POWERSCHOOL_CLIENT_ID,
	client_secret=POWERSCHOOL_CLIENT_SECRET
)

for _ in range(10):
	payload = {
		"students" : {
			"student" : {
				"client_uid": "ScholarOS",
				"action": "INSERT",
				"name": {
					"first_name": fake.first_name(),
					"last_name": fake.last_name(),
					"middle_name": ""
				},
				"demographics" : {
					"gender" :  fake.random_element(elements=('M', 'F')),
					"birth_date": fake.date_of_birth().strftime("%Y-%m-%d"),
				},
				"addresses" : {
					"physical" : {
						"street": fake.street_address(),
						"city": fake.city(),
						"state_province" : "AK",
						"postal_code" : fake.zipcode()
					}
				},
				"school_enrollment": {
					"grade_level": fake.random_int(min=1, max=5),
					"enroll_status": "A",
					"entry_date": fake.date_this_year().strftime("%Y-%m-%d"),
					"exit_date": "2025-06-30",
					"school_number": DUMMY_SCHOOL_NUMBER
				}
			}
		}
	}
	print(Fore.LIGHTCYAN_EX + json.dumps(payload, indent=4))
	response = powerschool.to('/ws/v1/student').with_data(payload).method("POST").send()
	student_data = json.loads(response.to_json())
	print(Fore.GREEN + json.dumps(student_data, indent=4))