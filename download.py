import os
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time
from tqdm import tqdm
import yaml


def fetch_page(base_url,year):
    # Construct the URL for the page based on the base URL and the year
    page_url = f"{base_url}{year}/"

    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, "Downloaded_Data")
    # Create a directory to store downloaded data if it doesn't exist
    os.makedirs(full_path,exist_ok=True)

    # Fetch the page content
    response = requests.get(page_url)

    # Check if the page was fetched successfully
    if response.status_code == 200:

        # Parse the page content with BeautifulSoup to extract links to CSV files
        soup = BeautifulSoup(response.content, "html.parser")
        links = [link.get('href') for link in soup.find_all('a', href=True) if link.get('href').endswith('.csv')]
        print("Page fetched successfully")
    else:
        # Raise an exception if the page was not fetched successfully
        raise Exception("Failed to fetch page")
    
    # Return the list of links to CSV files found on the page
    return links
    

async def download_file(url, file_name,pbar):
    # using aiohttp create a session and write response contents to csv files.

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_name, 'wb') as f:
                    f.write(await response.read())
                # updating the number of files downloaded (pbar is from tqdm which tracks) 
                pbar.update(1)
            else:
                print(f"Failed to download {url}")

async def download_data(links,base_url,year):
    tasks = []

    # create a dir for downloaded data
    current_dir = os.getcwd()
    year_folder_path = os.path.join(current_dir,"Downloaded_Data")
    os.makedirs(year_folder_path,exist_ok=True)

    with tqdm(len(links),desc="Downloading files") as pbar:
        for i, url in enumerate(links):
            full_url  = f"{base_url}/{str(year)}/{url}"
            # pile all the tasks that should be done asynchronously
            task = asyncio.create_task(download_file(full_url, os.path.join(year_folder_path,url),pbar))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__=="__main__":
    base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"

    with open('params.yaml','r') as file:
        params = yaml.safe_load(file)

    year = params['year']
    n_locs = params['n_locs']

    start_time = time.time()
    links = fetch_page(base_url,year)[-n_locs:-1]
    print(f"Fetch task finished in {time.time()-start_time} sec.")
    # perform asynchronous run
    asyncio.run(download_data(links,base_url,year))
    print("-"*100)
    print(f"Download task finished in {time.time()-start_time} sec.")
