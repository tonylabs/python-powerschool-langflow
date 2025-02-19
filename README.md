# PowerSchool Langflow
 
## Perquisites

- Python 3.8 or higher
- PowerSchool Adapter Library
- Chroma Database Python client library


## Text Embeddings

Embed dummy data which was generated by Python faker:

```text
{'embedding': [-0.6020767092704773, -0.7206705808639526, -2.4430699348449707, -0.6081189513206482, -0.3681376278400421, 0.30644160509109497, 0.8774333596229553, -1.1189463138580322, 1.1225370168685913, -0.03398386389017105, -0.9951059222221375, 0.05440517142415047, 1.6257606744766235, 0.06402243673801422, -0.13153652846813202, -0.5484852194786072, 0.40664592385292053, -0.3808309733867645, ..., -0.6412163972854614]
Payload sent to API: {'model': 'nomic-embed-text', 'prompt': "{'name': 'Hess, Travis', 'grade': '4', 'student_number': 'xxxxx', 'gender': 'Female', 'enroll_status': 'enrolled', 'district_entry_date': '2025-xx-xx', 'entry_date': '2025-xx-xx', 'exit_date': '2025-06-30', 'parents': {'father': 'Timothy Aguirre', 'mother': 'Patty Holmes'}} {'2025': {'tuition': '250885 RMB', 'capital_fee': '13248 RMB'}, '2024': {'tuition': '218220 RMB', 'capital_fee': '20417 RMB'}} [{'type': 'Lego Kit', 'checkout_date': datetime.date(2024, 4, 8)}, {'type': 'Camera', 'checkout_date': datetime.date(2024, 3, 28)}, {'type': 'History Book', 'checkout_date': datetime.date(2024, 9, 8)}, {'type': 'Chinese Book', 'checkout_date': datetime.date(2024, 10, 10)}] {'HepB': {'1st': datetime.date(2007, 12, 16), '2nd': datetime.date(2010, 5, 22), '3rd': datetime.date(2019, 6, 19)}, 'DTaP/Tdap': {'DTaP_series_completed': 'pre-age 7', 'Tdap_booster': datetime.date(2022, 7, 17)}}"}
```

---

## Langflow

Drag and drop a Chroma DB component with the following settings:

- Collection Name: students
- Persistence Directory: `/data/chroma`
- Search Query: connect to the `Chat Input` component
- Embedding: connect to an `Ollama Embeddings` component
- Search Results: connect to a`Parse Data` component