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

response = powerschool.table('students').projection(["ID", "DCID", "STUDENT_NUMBER", "LASTFIRST"]).set_method("GET").send().count()

student_data = json.loads(response.to_json())
print(Fore.GREEN + json.dumps(student_data, indent=4))