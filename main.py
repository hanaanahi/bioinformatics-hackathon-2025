import requests 
from google import genai
import os 
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API = os.getenv("GEMINI_API_KEY")

# https://clinicaltables.nlm.nih.gov/apidoc/snps/v3/doc.html
# outputs rsNum, 38.chr, 38.pos, 38.alleles, 38.gene
def find_snp(snp:str):
    try:
        url = "https://clinicaltables.nlm.nih.gov/api/snps/v3/search"
        params = {"terms": snp}

        res = requests.get(url, params=params, timeout=2)
        res.raise_for_status()
        return res

    except Exception as e:
        print(e)
        return None

def parse_results(data, query):
    table = data[3]

    for row in table:
        if row[0] == query:
            return {
                "rsid": row[0],
                "chromosome": row[1],
                "position": row[2],
                "alleles": row[3],
                "gene": row[4] if row[4] else None
            }
    return None


#https://rest.ensembl.org/documentation/info/vep_id_get
def ensemble_id(id: str, species: str):
    try:
        url = f"https://rest.ensembl.org/vep/{species}/id/{id}"
        headers = {"Content-Type": "application/json"}
        res = requests.get(url,headers= headers, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(e)
        return None

def ensemble_gene(gene: str, species: str):
    try:
        url = f"https://rest.ensembl.org/lookup/symbol/{species}/{gene}"
        headers = {"Content-Type": "application/json"}
        res = requests.get(url, headers= headers, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(e)
        return None

def ensemble_gene_variant(gene_res):
    if gene_res is None:
        print("No gene info provided.")
        return None
    try:
        start = gene_res["start"]
        end = gene_res["end"]
        seq = gene_res["seq_region_name"]
        species = gene_res["species"]
        place = f"{seq}:{start}-{end}"
        url = f"https://rest.ensembl.org/overlap/region/{species}/{place}?feature=variation"
        headers = {"Content-Type": "application/json"}
        res = requests.get(url, headers= headers, timeout=10)
        res.raise_for_status()
        return res.json()

    except Exception as e:
        print(e)
        return None



def find_snp(snp:str):
    try:
        url = "https://clinicaltables.nlm.nih.gov/api/snps/v3/search"
        params = {"terms": snp}

        res = requests.get(url, params=params, timeout=2)
        res.raise_for_status()
        return res.json()

    except Exception as e:
        print(e)
        return None
    
def parse_results(data, query):
    table = data[3]

    for row in table:
        if row[0] == query:
            return {
                "rsid": row[0],
                "chromosome": row[1],
                "position": row[2],
                "alleles": row[3],
                "gene": row[4] if row[4] else None
            }
    return None


# myvariant.info
# for SNP: https://myvariant.info/v1/variant/<snp>
# for gene ID: https://myvariant.info/v1/gene/<geneID>
def myvariant_query(query:str):

    # check if the query is for a SNP or gene ID
    if (query.startswith("rs")):
        # SNP query
        type = "variant"
    else:
        # gene query
        type = "gene"

    # build the request url
    #   "?fields=<list of specified fields>" filters out relevant fields
    #   "dotfield=true" flattens the returned data object (makes it easier for the llm to read)
    #   "size=5" returns 5 known variants
    fields = "clinvar,dbnsfp,cadd,cosmic,hgvs,gene,refseq,ensembl"
    url = f"https://myvariant.info/v1/{type}/{query}?fields={fields}&dotfield=true&size=5"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(e)
        return None


def ai_summary(json_data):
    client = genai.Client(api_key=GOOGLE_API)

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        # TODO: finetune prompt so it's more helpful (goals: functional role, disease association, + known variants)
        contents=f"Summarize the following JSON data of a gene or SNP:{json_data}"
    )
    return response.text


if __name__ == "__main__":
    query = input("enter gene symbol!")

    print(f"searching for {query}")

    #print("clinicaltables: ", find_snp(query))
    print("myvariant: ", myvariant_query(query))

    #print("ai summary: ", ai_summary(myvariant_query(query)))