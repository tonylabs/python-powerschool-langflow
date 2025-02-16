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

# Load sensitive data from environment variables
SERVER_ADDRESS = os.getenv("POWERSCHOOL_SERVER_ADDRESS")
CLIENT_ID = os.getenv("POWERSCHOOL_CLIENT_ID")
CLIENT_SECRET = os.getenv("POWERSCHOOL_CLIENT_SECRET")

powerschool = PowerSchool(
    server_address=SERVER_ADDRESS,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

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
				"school_number": 3
			}
		}
	}
}

print(Fore.LIGHTCYAN_EX + json.dumps(payload, indent=4))

response = powerschool.to('/ws/v1/student').with_data(payload).method("POST").send()
student_data = json.loads(response.to_json())
print(Fore.GREEN + json.dumps(student_data, indent=4))