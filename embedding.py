import requests

def create_embeddings(text):
	"""
    Sends paragraphs to the locally running Ollama API for embedding creation.

    Args:
        paragraphs (list of str): A list of paragraphs to embed.

    Returns:
        list: A list of embedding vectors.
    """
	# Define the API URL
	url = "https://deciding-horribly-robin.ngrok-free.app/api/embeddings"

	# Prepare the payload
	payload = {
		"model": "nomic-embed-text", # https://ollama.com/library/nomic-embed-text
		"prompt": "\n".join(text)  # Combine paragraphs into a single prompt if needed
	}

	# Make the HTTP POST request
	response = requests.post(url, json=payload)

	print(text)
	print(response.json().get("embedding"))

	# Check for successful response
	if response.status_code == 200:
		return response.json().get("embedding")
	else:
		raise Exception(f"Failed to get embeddings: {response.status_code}, {response.text}")