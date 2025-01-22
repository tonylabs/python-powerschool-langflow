import os
import requests
from dotenv import load_dotenv

load_dotenv()
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")

def create_embeddings(text):
	"""
    Sends paragraphs to the locally running Ollama API for embedding creation.

    Args:
        paragraphs (list of str): A list of paragraphs to embed.

    Returns:
        list: A list of embedding vectors.
    """
	# Prepare the payload
	payload = {
		"model": "nomic-embed-text", # https://ollama.com/library/nomic-embed-text
		#"prompt": "\n".join(text)  # Combine paragraphs into a single prompt if needed
		"prompt": text
	}

	# Make the HTTP POST request
	response = requests.post(EMBEDDING_API_URL, json=payload)

	print(f"Payload sent to API: {payload}")
	#print(f"Response Status Code: {response.status_code}")
	#print(f"Response JSON: {response.json()}")
	#print(response.json().get("embedding"))

	# Check for successful response
	if response.status_code == 200:
		return response.json().get("embedding")
	else:
		raise Exception(f"Failed to get embeddings: {response.status_code}, {response.text}")