rs_num = 6311
import get_ensembl, requests
import pandas as pd

data = requests.get(f"https://api.ncbi.nlm.nih.gov/variation/v0/refsnp/{rs_num}", timeout=30).json()
#df = pd.read_json(data)
print(data)