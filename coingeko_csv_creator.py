import requests
import csv
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def web_scrapper(url):      #scrapes the websites to search for keyword "api" and returns the url with that word
    if url:
        try:
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            for a_tag in soup.findAll('a'):
                try:
                    full_text = a_tag.text.lower()
                    if full_text.find("api") != -1:
                        href = a_tag.attrs.get("href")
                        if href == "" or href is None:
                            # href empty tag
                            continue
                        # join the URL if it's relative (not absolute link)
                        href = urljoin(url, href)
                        parsed_href = urlparse(href)
                        # remove URL GET parameters, URL fragments, etc.
                        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                        return href
                except:
                    return ""
        except:
            return ""
                    
def get_id_list():  #gets all the id from coingeko exchange list api to use in the details of exchanges
    url = "https://api.coingecko.com/api/v3/exchanges/list"
    r = requests.get(url).json()
    final_list = []

    for x in range(418):
        final_list.append(r[x]["id"])
    return final_list

def exchange_details_to_csv():    #creates the csv file using the details and return value of webscrapper function
    id_list = get_id_list()
    with open('exchangeDetails.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["S.No", "EXCHANGE_NAME", "WEBSITE_URL","Centralized", "API_URL", "API_URL"])
        
        for x in range(len(get_id_list())):
            url = "https://api.coingecko.com/api/v3/exchanges/" + str(id_list[x])
            r = requests.get(url).json()
            api_url = web_scrapper(r["url"])
            writer.writerow([str(x+1), r["name"], r["url"], r["centralized"], api_url])
            print('Added: ' + r['url'])
            print('Found: ' + str(api_url))
            time.sleep(0.5)
    
exchange_details_to_csv()

#print(web_scrapper("https://www.coingecko.com/en"))
