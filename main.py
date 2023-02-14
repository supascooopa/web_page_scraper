import csv
import requests
from bs4 import BeautifulSoup
import re


# This part is for copying a webpage I'm interested in so that I don't keep making requests
def get_webpage_copy(url, file_name="generic.html"):
    """Writes a given url to html file"""
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"}
    data = requests.get(url, headers=headers)
    with open(file_name, "w") as f:
        f.write(data.text)


webpage_url = "https://jamesclear.com/best-books/best-selling"

with open("generic.html") as web_page_copy:
    soup = BeautifulSoup(web_page_copy, "html.parser")
rows = soup.findAll("p")
clean_rows = [cleaned for cleaned in rows if "#" in cleaned.get_text()]
new_rows = []
for item in clean_rows:
    item_text = item.get_text()
    rank = re.search(r"#\d+", item_text).group().strip("#")
    title = re.search(r"–(.*)\(", item_text).group(1)
    sales_numbers = re.search(r"\d+\s\w+", item_text).group()
    written_by = re.search("by(.*)P", item_text).group(1)
    print(written_by, item_text)
    new_rows.append([rank, title, sales_numbers, written_by])

with open("best_sellers.csv", "w") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(new_rows)


