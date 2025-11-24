from easy_entrez import EntrezAPI



entrez_api = EntrezAPI(
    'SNPchatbot',
    'heatherho@gmail.com',
    # optional
    return_type='json'
)

# find up to 10 000 results for cancer in human
result = entrez_api.search('cancer AND human[organism]', max_results=10_000)

# data will be populated with JSON or XML (depending on the `return_type` value)
result.data

