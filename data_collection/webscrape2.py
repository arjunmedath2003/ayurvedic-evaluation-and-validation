from playwright.async_api import async_playwright
import asyncio
import pandas as pd
import os
from protein_map2 import driver

# List of plants to process
# options = ["Woodfordia fruticosa","Vitis vinifera"]
plants=['Mesua ferrea', 'Saccharum officinarum', 'Gmelina arborea', 'Phyllanthus emblica', 'Embelia ribes', 'Sida cordifolia', 'Tinospora sinensis', 
        'Nelumbo nucifera', 'Myristica fragrans', 'Zingiber officinale', 'Piper nigrum', 'Areca catechu', 'Terminalia arjuna', 'Curcuma longa', 
        'Madhuca longifolia', 'Cinnamomum verum', 'Rubia cordifolia', 'Berberis aristata', 'Asparagus racemosus', 'Vitis vinifera', 'Piper longum', 
        'Cinnamomum tamala', 'Nymphaea nouchali', 'Tribulus terrestris', 'Elettaria cardamomum', 'Bacopa monnieri', 'Glycyrrhiza glabra', 
        'Holarrhena pubescens', 'Acacia catechu', 'Cyperus rotundus', 'Terminalia chebula', 'Aloe vera', 'Woodfordia fruticosa', 'Justicia adhatoda', 
        'Chrysopogon zizanioides', 'Symplocos racemosa', 'Cuminum cyminum', 'Santalum album', 'Saraca asoca', 'Withania somnifera']
options=plants[33:]
# 40
async def main():
    async with async_playwright() as pw:
        # Launch headless=False to watch it work
        browser = await pw.chromium.launch(headless=False) 
        
        for plant_name in options:
            page = await browser.new_page()
            # Set a longer timeout for navigation
            await page.goto("https://cb.imsc.res.in/imppat/", wait_until="domcontentloaded", timeout=90000)

            dropdown = page.locator(
                "div.container div.sectionhomepage div#browse div.sectiondropdown.shadow.bg-drop1.p-3.border.rounded div.form-group.p-2"
            ).nth(0).locator("select.homeselect.form-control")
            
            await dropdown.select_option(plant_name)

            # Wait for the main phytochemical table to appear
            await page.locator("table#table_id").wait_for(timeout=30000)
            await page.wait_for_load_state('networkidle')

            phytochemical_data = []
            page_count=0
            while True:
                # Find all rows on the *current page*
                rows = page.locator("table#table_id tbody tr")
                count = await rows.count()

                for r in range(count):
                    # Re-fetch rows locator to avoid stale element issues
                    while True:
                        rows = page.locator("table#table_id tbody tr")
                        link = rows.nth(r).locator("td:nth-of-type(4) a")

                        if not await link.is_visible():
                            continue

                        name = (await link.inner_text()).strip()
                        phytochemical_data.append(name)
                        break
                # --- Pagination Logic ---
                next_button = page.locator("#table_id_next")
                page_count+=1
                if not await next_button.is_visible():
                    break  

                button_class = await next_button.get_attribute("class")
                if button_class and "disabled" in button_class:
                    print("Last page reached.")
                    break  # We are on the last page
                
                print("Clicking 'Next' page...")
                await next_button.click()
                await page.wait_for_load_state("networkidle")
                await page.locator("table#table_id tbody").wait_for(timeout=30000)

            # --- Save to CSV ---
            os.makedirs("proteins", exist_ok=True)
            df = pd.DataFrame(phytochemical_data,columns=['Phytos'])
            output_path = f"proteins/{plant_name.replace(' ', '_').lower()}.csv"
            df.to_csv(output_path, index=False)
            print(f"--- SCRIPT FINISHED ---")
            print(f"Saved data for {plant_name} to {output_path}")
            await page.close()
        await browser.close()

# asyncio.run(main())

for name in options:
    print(f"{name} started")
    driver(name)

# ["Cinnamomum tamala", "Nymphaea nouchali" ] 