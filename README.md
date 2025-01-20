# PowerSchool Langflow
 
## Perquisites

- Python 3.8 or higher
- PowerSchool API Python client library
- astrapy Python client library

## Create SSH Tunnel

```bash
ssh -N -L 8000:10.211.152.74:8000 tony@3.tcp.ngrok.io -p 24137
```

## Langflow

Drag and drop a Chroma DB component with the following settings:

- Collection Name: students
- Persistence Directory: `/data/chroma`
- Search Query: connect to the `Chat Input` component
- Embedding: connect to an `Ollama Embeddings` component
- Search Results: connect to a`Parse Data` component