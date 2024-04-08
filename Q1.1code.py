#import modules for web scraping. 
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#search for a specfic pattern within a movie url.
def extract_movie_id(url):
    match = re.search(r'gr(\d+)/', url)
    if match:
        group_id = match.group(1)
        return "gr" + group_id
    else:
        return None
#scrap data from website BoxOfficeMojo.
if __name__ == "__main__":
    
    url = f"https://www.boxofficemojo.com/year/world/2023/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', class_='mojo-body-table') #find all tables that have the class attribute to 'mojo body table'
        if tables:
            with open("TopMoviesBoxOffice.txt", "w", encoding="utf-8") as file:
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        columns = row.find_all('td')
                        if columns:
                            rank = columns[0].text.strip() 
                            movie_name = columns[1].text.strip().replace(",", "")
                            movie_url = columns[1].find('a')['href']
                            movie_id = extract_movie_id(movie_url)
                            worldwide_boxoffice = columns[2].text.strip().replace(",", "").replace("$", "")
                            domestic_boxoffice = columns[3].text.strip().replace(",", "").replace("$", "")
                           
                            file.write(f"{rank},{movie_name},{movie_id},{worldwide_boxoffice},{domestic_boxoffice}\n") #a formatted string to the file, extract value of 5 items
        print("TopMoviesBoxOffice.txt")
