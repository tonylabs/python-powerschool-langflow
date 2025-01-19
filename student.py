import os
import chromadb
from chromadb import Collection
import powerschool
import embedding
from dotenv import load_dotenv

load_dotenv()

chroma_client = chromadb.HttpClient(host='10.211.152.75', port=8000)

def vectorize_students(collection: Collection, embedding_string_creator: callable) -> None:

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
		'q': 'enroll_status=ge=0',
		'projection': 'dcid,schoolid,student_number,lastfirst,last_name,first_name,grade_level,gender,districtentrydate,entrydate,exitdate,father,mother,enroll_status',
	}
	array_students = students_table.query(**params).pagesize(1)

	# Define the list of students and their attributes
	students = [
		{
			"student_id": student['dcid'],
			"name": student['lastfirst'],
			"metadata": {
				"SCHOOL ID": student['schoolid'],
				"STUDENT NUMBER": student['student_number'],
				"LAST NAME": student['last_name'],
				"FIRST NAME": student['first_name'],
				"GENDER": 'Female' if student['gender'] == 'F' else 'Male',
				"GRADE LEVEL": student['grade_level']
			},
			"$vector": embedding.create_embeddings(embedding_string_creator(student)),
		}
		for student in array_students
	]

	print(students)
	exit()

	# Add documents to the collection
	for student in students:
		collection.add(
			ids=[student["student_id"]],
			documents=[student["content"]],
			metadatas=[student["metadata"]],
			embeddings=[student["$vector"]]
		)


def main():
	print(chroma_client.heartbeat())
	print(chroma_client.get_version())
	print(chroma_client.list_collections())

	# Create or get a collection
	collection_name = "students"
	collection = chroma_client.get_or_create_collection(name=collection_name)

	vectorize_students(
		collection,
		lambda data: (
			f"STUDENT NAME: {data['lastfirst']} | "
		),
	)


if __name__ == "__main__":
	main()