from re import I
import aiohttp
import asyncio
import pandas as pd
from urllib.parse import quote
from pkg_resources import safe_name
from tqdm.asyncio import tqdm_asyncio


BASE = "https://www.ebi.ac.uk/chembl/api/data"
MAX_CONCURRENT = 10  # safe for ChEMBL

async def retry(coro_func, retries=5, delay=0.5):
    for attempt in range(retries):
        try:
            result = await coro_func()
            if result:
                return result
        except Exception:
            pass
        await asyncio.sleep(delay)
    return None

# ------------------ ASYNC HELPERS ------------------

async def fetch_json(session, url, sem):
    async with sem:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {}
            return await resp.json()

# ------------------ CORE FUNCTIONS ------------------

async def get_phyto_chembl_id(session, phyto, sem, cache):
    if phyto in cache:
        return cache[phyto]

    async def task():
        url = f"{BASE}/molecule/search?q={quote(phyto)}&format=json"
        res = await fetch_json(session, url, sem)
        return res["molecules"][0]["molecule_chembl_id"]

    mol_id = await retry(task, retries=5)

    cache[phyto] = mol_id
    return mol_id


async def get_target_chembl_ids(session, mol_id, sem):
    async def task():
        url = (
            f"{BASE}/activity.json?"
            f"molecule_chembl_id={mol_id}"
            f"&target_organism=Homo%20sapiens"
            f"&confidence_score__gte=4"
            f"&limit=1000"
        )
        res = await fetch_json(session, url, sem)
        return list({i["target_chembl_id"] for i in res.get("activities", [])})

    targets = await retry(task, retries=5)
    return targets or []


async def get_gene_name(session, target_id, sem, cache):
    if target_id in cache:
        return cache[target_id]

    async def task():
        url = f"{BASE}/target/{target_id}.json"
        res = await fetch_json(session, url, sem)

        if res.get("target_type") == "SINGLE PROTEIN":
            for comp in res.get("target_components", []):
                for syn in comp.get("target_component_synonyms", []):
                    if syn.get("syn_type") == "GENE_SYMBOL":
                        return syn.get("component_synonym")
        return None

    gene = await retry(task, retries=5)
    cache[target_id] = gene
    return gene

import re
import hashlib

def safe_filename(name, max_len=100):
    # remove illegal characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.replace(" ", "_")

    # hash long chemical names (recommended)
    if len(name) > max_len:
        h = hashlib.md5(name.encode()).hexdigest()[:10]
        name = name[:50] + "_" + h

    return name


# ------------------ DRIVER ------------------

async def driver_async(name):
    # name = name.lower().replace(" ", "_")
    # data = pd.read_csv(f"phytochemicals/{name}.csv")

    sem = asyncio.Semaphore(MAX_CONCURRENT)
    mol_cache = {}
    gene_cache = {}
    proteins = set()

    async with aiohttp.ClientSession() as session:

        # 1️⃣ Molecule IDs
        mol_tasks = [
            get_phyto_chembl_id(session, name.lower(), sem, mol_cache)
        ]
        mol_ids = [
            m for m in await tqdm_asyncio.gather(
                *mol_tasks,
                desc="Fetching ChEMBL Molecules"
            )
            if m
        ]

        if not mol_ids:
            return

        # 2️⃣ Target IDs
        target_tasks = [
            get_target_chembl_ids(session, mol_id, sem)
            for mol_id in mol_ids
        ]
        target_lists = await tqdm_asyncio.gather(
            *target_tasks,
            desc="Fetching Human Targets"
        )
        target_ids = set(t for sub in target_lists for t in sub)

        if not target_ids:
            return

        # 3️⃣ Gene symbols
        gene_tasks = [
            get_gene_name(session, tid, sem, gene_cache)
            for tid in target_ids
        ]
        genes = await tqdm_asyncio.gather(
            *gene_tasks,
            desc="Resolving Gene Symbols"
        )
        proteins.update(
            g.strip()
            for g in genes
            if isinstance(g, str) and g.strip()
        )
        
        if not proteins:
            print(f"No proteins found for {name}. Skipping CSV creation.")
            return

        df = pd.DataFrame(sorted(proteins), columns=["Protein"])
        if len(df)>0: df.to_csv(f"proteins2/{safe_name(name)}.csv", index=False)

# ------------------ RUN ------------------

def driver(name):
    asyncio.run(driver_async(name))