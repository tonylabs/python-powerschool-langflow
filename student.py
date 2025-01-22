import os
import random
import chromadb
from chromadb import Collection
import powerschool
import requests
import embedding
from dotenv import load_dotenv
from faker import Faker
import colorama
from colorama import Fore, Back

load_dotenv()
fake = Faker()
colorama.init(autoreset=True)

CHROMA_DB_HOST = os.getenv("CHROMA_DB_HOST")
CHROMA_DB_PORT = os.getenv("CHROMA_DB_PORT")
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")

chroma_client = chromadb.HttpClient(host=CHROMA_DB_HOST, port=CHROMA_DB_PORT)

def vectorize_students(collection: Collection) -> None:

	if (os.getenv('PS_CLIENT_ID') is None or
			os.getenv('PS_CLIENT_SECRET') is None or
			os.getenv('PS_HOST') is None):
		print("Environment variables were not set.")
		exit()

	client_id = os.getenv("PS_CLIENT_ID")
	client_secret = os.getenv("PS_CLIENT_SECRET")
	credentials = (client_id, client_secret)
	ps = powerschool.PowerSchool(os.getenv('PS_HOST'), auth=credentials)

	students_table = ps.get_schema_table('students')
	params = {
		'q': 'enroll_status==0',
		'pagesize': 10,
		'page': 1,
		'projection': 'dcid,schoolid,student_number,lastfirst,last_name,first_name,grade_level,gender,districtentrydate,entrydate,exitdate,father,mother,enroll_status',
	}
	array_students = students_table.query(**params)

	for student in array_students:
		# Generate a fake 4-digit student number
		student_number = fake.random_int(min=1000, max=9999)

		# Enrollment status
		enroll_status = "enrolled"

		# Generate tuition and capital fees for the year 2025
		tuition_fee_2025 = fake.random_int(min=100000, max=300000)
		capital_fee_2025 = fake.random_int(min=10000, max=30000)

		# Generate tuition and capital fees for the year 2024
		tuition_fee_2024 = fake.random_int(min=100000, max=300000)
		capital_fee_2024 = fake.random_int(min=10000, max=30000)

		# Generate student name and gender
		student_name = (
			fake.name_female() if student["gender"] == "F" else fake.name_male().replace(" ", ", ")
		)
		gender = "Female" if student["gender"] == "F" else "Male"

		# Generate parent names
		father_name = fake.name_male()
		mother_name = fake.name_female()

		# Create the student profile
		student_profile = {
			"name": student_name,
			"grade": student["grade_level"],
			"student_number": student_number,
			"gender": gender,
			"enroll_status": enroll_status,
			"district_entry_date": student["districtentrydate"],
			"entry_date": student["entrydate"],
			"exit_date": student["exitdate"],
			"parents": {"father": father_name, "mother": mother_name},
		}

		# Create the billing profile
		billing_profile = {
			"2025": {"tuition": tuition_fee_2025, "capital_fee": capital_fee_2025},
			"2024": {"tuition": tuition_fee_2024, "capital_fee": capital_fee_2024},
		}

		# Generate checked-out school properties
		school_devices = ["Macbook", "iPad", "Lego Kit", "Calculator", "Headphones", "Camera"]
		school_books = ["Math Book", "Science Book", "History Book", "English Book", "Chinese Book", "Art Book"]
		selected_devices = random.sample(school_devices, 2)
		selected_books = random.sample(school_books, 2)

		checkout_properties = [
								  {"type": device,
								   "checkout_date": fake.date_between(start_date="-1y", end_date="today")}
								  for device in selected_devices
							  ] + [
								  {"type": book, "checkout_date": fake.date_between(start_date="-1y", end_date="today")}
								  for book in selected_books
							  ]

		# Create the vaccination profile
		vaccination_profile = {
			"HepB": {
				"1st": fake.date_between(start_date="-20y", end_date="-15y"),
				"2nd": fake.date_between(start_date="-15y", end_date="-10y"),
				"3rd": fake.date_between(start_date="-10y", end_date="-5y"),
			},
			"DTaP/Tdap": {
				"DTaP_series_completed": "pre-age 7",
				"Tdap_booster": fake.date_between(start_date="-5y", end_date="today"),
			},
		}

		# Combine the profiles into a single document
		combined_profile = f"{student_profile} {billing_profile} {checkout_properties} {vaccination_profile}"

		# Add the combined document to the collection
		collection.add(
			documents=[combined_profile],
			metadatas=[{"source": "student and billing profile"}],
			embeddings=[embedding.create_embeddings(combined_profile)],
			uris=[f"student_{student_number}"],
			ids=[student['dcid']]
		)


def query(collection: Collection, query_text):
	"""
	Queries the Chroma collection using embeddings generated by the Ollama API.

	Args:
		collection (Collection): The Chroma collection to query.
		query_text (str): The text query to embed and search in the collection.

	Returns:
		dict: The query results from Chroma.
	"""

	payload = {
		"model": "nomic-embed-text",  # Using the same model as in create_embeddings
		"prompt": query_text  # Use the query text directly
	}
	response = requests.post(EMBEDDING_API_URL, json=payload)
	if response.status_code == 200:
		query_embedding = response.json().get("embedding")
		if not query_embedding:
			raise ValueError("Embedding not found in API response.")

		# Query the Chroma collection with the embedding
		results = collection.query(
			query_embeddings=[query_embedding],  # Use the embedding for the query
			n_results=2  # Adjust the number of results as needed
		)
		return results
	else:
		raise Exception(f"Failed to get embeddings: {response.status_code}, {response.text}")


def main():
	print(Back.BLACK + Fore.LIGHTYELLOW_EX + f"Chroma Heartbeat: {chroma_client.heartbeat()}")
	print(Back.BLACK + Fore.LIGHTCYAN_EX + f"Chroma Version: {chroma_client.get_version()}")
	print(Back.BLACK + Fore.LIGHTYELLOW_EX + f"Chroma Collections: {chroma_client.list_collections()}")

	# Check if "students" collection exists before attempting to delete it
	if "students" in chroma_client.list_collections():
		chroma_client.delete_collection("students")
		print(Back.BLACK + Fore.LIGHTYELLOW_EX + f"Students collection has been deleted.")
	else:
		print(Back.BLACK + Fore.LIGHTYELLOW_EX + f"Students collection does not exist.")

	# Create or get a collection
	collection_name = "students"
	collection = chroma_client.get_or_create_collection(name=collection_name)
	print(Back.BLACK + Fore.LIGHTGREEN_EX + f"Students collection has been created or retrieved.")

	vectorize_students(collection)

	all_data = collection.get(
		limit=1
	) 
	print(Back.BLACK + Fore.LIGHTMAGENTA_EX + f"Retrieving the first 2 records as examples from Chroma DB: {all_data}")

	print(Back.BLACK + Fore.LIGHTRED_EX + f"Querying the database and searching for a record that is not from the examples:")
	results = query(collection, "Who is Chong, Hannah?")
	print(Back.BLACK + Fore.LIGHTGREEN_EX + f"Results: {results}")

if __name__ == "__main__":
	main()