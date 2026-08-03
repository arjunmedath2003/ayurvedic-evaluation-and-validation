import requests
import time

def get_genes_from_uniprot(protein_names, batch_size=50):
    url = "https://rest.uniprot.org/uniprotkb/search"
    
    gene_map=[]
    for i in range(0, len(protein_names), batch_size):
        batch = protein_names[i:i + batch_size]
        query = " OR ".join(batch)
        params = {
            "query": query,
            "fields": "accession,gene_primary,protein_name",
            "format": "json",
            "size": batch_size
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 400:
            print(f"Skipping batch {i//batch_size + 1}: Bad request")
            continue 
        response.raise_for_status()
        data = response.json()

        for result in data.get('results', []):
            protein_info = result.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', '')
            gene_info = result.get('genes', [{}])[0].get('geneName', {}).get('value', None)
            if protein_info and gene_info:
                gene_map.append(gene_info)
        time.sleep(0.2)
    
    return gene_map

def kegg_from_enrichr(protein_names,library="KEGG_2021_Human"):
    genes = get_genes_from_uniprot(protein_names)
    payload = {"list": "\n".join(genes), "description": "Gene set"}
    add_resp = requests.post("https://maayanlab.cloud/Enrichr/addList", files=payload)
    user_list_id = add_resp.json()["userListId"]

    enrich_url = f"https://maayanlab.cloud/Enrichr/enrich"
    params = {"userListId": user_list_id, "backgroundType": library}
    enrich_resp = requests.get(enrich_url, params=params)
    data = enrich_resp.json()[library]

    sorted_data = sorted(data, key=lambda x: x[2])
    return [(d[1], d[2], d[5]) for d in sorted_data]

# ls1=['TYR', 'CASP9', 'CASP8', 'CASP7', 'CSNK2A1', 'MMP2', 'CCL2', 'PRKCB', 'PRKACA', 'SYK', 'PARG', 'PRKCA', 'KEAP1', 'MAPK1', 'SERPINE1', 'CCND1', 'CCNB1', 'CDK4', 'CDK2', 'TNFRSF10B', 'NOTCH1', 'MITF', 'MAP2K1', 'DDIT4', 'NFKBIB', 'PKM', 'GSK3B', 'MAPK8', 'MCL1', 'MMP9', 'PLAU', 'CDK1', 'NFE2L2', 'ABCC1', 'RELA', 'SRC', 'AFP', 'TGFB1', 'PTK2', 'TLR4', 'NFAT5', 'NAMPT', 'HMGB1', 'TOP1', 'TOP2A', 'ICAM1']
# print(kegg_from_enrichr(ls1))
# genes = list(map(get_gene_name_from_uniprot,ls1))