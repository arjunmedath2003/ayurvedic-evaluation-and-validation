import pandas as pd
import pickle
import json

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

with open("ayurveda.json","rb") as file:
    ayurveda_data = json.load(file)

def save_protein_link(ayurveda):
    plants=ayurveda_data[ayurveda]['ingredients']
    proteins=[]
    for i in plants:
        df = pd.read_csv(f"proteins/{i.lower().replace(' ','_')}.csv")
        proteins+=df['Protein'].tolist()
    df = create_protein_link(proteins)
    df.to_csv(f"protein_links/{ayurveda}.csv",index=False)

ayurveda = ayurveda_data.keys()
for i in ayurveda:
    print(f"{i} started ")
    save_protein_link(i)
    print(f"{i} ended ")

# plants=['Acacia catechu', 'Aloe vera', 'Areca catechu', 'Asparagus racemosus', 
#         'Bacopa monnieri', 'Berberis aristata', 'Chrysopogon zizanioides',
#         'Cinnamomum tamala', 'Cinnamomum verum', 'Cuminum cyminum', 'Curcuma longa', 
#         'Cyperus rotundus', 'Elettaria cardamomum', 'Embelia ribes', 
#         'Glycyrrhiza glabra', 'Gmelina arborea', 'Holarrhena pubescens', 
#         'Justicia adhatoda', 'Madhuca longifolia', 'Mesua ferrea', 'Myristica fragrans', 
#         'Nelumbo nucifera', 'Nymphaea nouchali', 'Phyllanthus emblica', 'Piper longum', 
#         'Piper nigrum', 'Rubia cordifolia', 'Saccharum officinarum', 'Santalum album', 
#         'Saraca asoca', 'Sida cordifolia', 'Symplocos racemosa', 'Terminalia arjuna', 
#         'Terminalia chebula', 'Tinospora sinensis', 'Tribulus terrestris', 'Vitis vinifera', 
#         'Withania somnifera', 'Woodfordia fruticosa', 'Zingiber officinale']