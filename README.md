# PowerSchool Langflow
 
## Perquisites

- Python 3.8 or higher
- PowerSchool Adapter Library
- Chroma Database Python client library

## Langflow

Drag and drop a Chroma DB component with the following settings:

- Collection Name: students
- Persistence Directory: `/data/chroma`
- Search Query: connect to the `Chat Input` component
- Embedding: connect to an `Ollama Embeddings` component
- Search Results: connect to a`Parse Data` component
