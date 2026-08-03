import pandas as pd
import pickle

def create_protein_link(proteins):
    protein_link_dict=[]
    with open("protein_link_dict.pkl", "rb") as file:
        protein_link_dict = pickle.load(file)
    protein_list=[]
    for i in proteins:
        if i not in protein_list: protein_list.append(i)
    n = len(protein_list)
    info = pd.read_csv("..\string\9606.protein.info.v12.0.txt",sep='\t', encoding='utf-8')
    info_dict = dict(zip(info['preferred_name'], info['#string_protein_id']))
    df = pd.DataFrame(columns=["Protein1", "Protein2", "Score"])
    for i in range(n-1):
        try:
            protein_1 = protein_list[i]
            id1 = info_dict[protein_1]
            for j in range(i+1, n):
                try:
                    protein_2 = protein_list[j]
                    id2 = info_dict[protein_2]
                    # print(id1,id2)
                    score = protein_link_dict.get(id1, {}).get(id2)
                    if score:
                        # print(f"Success for protein {protein_2}")
                        score = score/1000
                        df.loc[len(df)] = [protein_1, protein_2, score]
                        # print(f"Score of {protein_1} and {protein_2} is {score}")
                except: pass
        except:
            pass
    return df