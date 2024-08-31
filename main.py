from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv


def read_csv(file):
    tracks_to_search = []
    with open(file, "r", newline="") as file:
        reader = csv.reader(file, delimiter=';')
        title_row = next(reader)
        # create a list of tuples (rows of data)
        for row in reader:
            tracks_to_search.append(tuple(row))  # convert to tuple for future convertion into set
    return tracks_to_search


def write_csv(result):
    with open('result_list.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(result)


driver = Chrome()
driver.maximize_window()

base_url = 'https://www.beatport.com'
url = 'https://www.beatport.com/search/tracks?q='


def search_track(track_to_search):
    driver.get(url + track_to_search)
    search_results_source = driver.page_source
    results_soup = BeautifulSoup(search_results_source, "html.parser")
    track_url = (results_soup.find('div', class_="Table-style__TableCell-sc-fdd08fbd-0 iqwxwW cell title")
                             .find("a").get("href"))
    return track_url


def find_track_time(track_url):
    driver.get('https://www.beatport.com' + track_url)
    track_page = driver.page_source
    track_soup = BeautifulSoup(track_page, "html.parser")
    track_length = (track_soup.find("div", class_="TrackMeta-style__MetaItem-sc-9c332570-0 hpiTYE")
                              .find("span").text)
    return track_length


tracks_to_search = read_csv('tracks.csv')
result_list = []
for track in tracks_to_search:
    track_to_search = '+'.join(track).replace(" ", "+")
    track_url = search_track(track_to_search)
    track_length = find_track_time(track_url)
    result_list.append((track[0], track[1], track_length))
    pass

write_csv(result_list)
