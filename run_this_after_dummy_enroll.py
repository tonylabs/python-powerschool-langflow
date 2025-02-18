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

# Load sensitive data from environment variables
POWERSCHOOL_SERVER_ADDRESS = os.getenv("POWERSCHOOL_SERVER_ADDRESS")
POWERSCHOOL_CLIENT_ID = os.getenv("POWERSCHOOL_CLIENT_ID")
POWERSCHOOL_CLIENT_SECRET = os.getenv("POWERSCHOOL_CLIENT_SECRET")

powerschool = PowerSchool(
	server_address=POWERSCHOOL_SERVER_ADDRESS,
	client_id=POWERSCHOOL_CLIENT_ID,
	client_secret=POWERSCHOOL_CLIENT_SECRET
)

response = powerschool.table('students').projection(["DCID", "STUDENT_NUMBER", "LASTFIRST"]).set_method("GET").send()
students = json.loads(response.to_json())
print(Fore.GREEN + json.dumps(students, indent=4))