from clustering import createncluster
from kegg import kegg_from_enrichr
from datetime import datetime
import json
import pandas as pd
from protein_link import create_protein_link

inp = input("Enter formula name: ")
with open("ayurveda.json", "r", encoding="utf-8") as f:
    ayurveda = json.load(f)

plants = ayurveda[inp.lower()]["ingredients"]
plants = [i.strip().replace(" ","_") for i in plants]
print("Ingredients: "," ".join(plants))

kegg_pathways = []
proteins=[]
for plant in plants:
    ds = pd.read_csv(f"proteins/{plant}.csv")
    proteins+=ds['Protein'].tolist()

print("Creating protein link scores")
df = create_protein_link(proteins)

print("Creating cluster")
temp_cluster = createncluster(proteins,df)
cluster = [i for i in temp_cluster if len(i)>1]
print(f"{len(cluster)} clusters")

print("Pathway calculation started")
for num,each in enumerate(cluster):
    print(f"Cluster {num+1} started")
    temp = kegg_from_enrichr(each)
    kegg_pathways+=temp[:10]

now = datetime.now()
datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

with open(f"{str(datetime_str)}.txt","w") as file:
    for i,j,k in kegg_pathways:
        string = i+" - "+str(j)+" - "+str(k)+"\n"
        file.write(string)