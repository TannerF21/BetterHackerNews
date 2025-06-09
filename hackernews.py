import requests
from bs4 import BeautifulSoup
import pprint

def fetch_hn_page(page_num):
    url = f"https://news.ycombinator.com/news?p={page_num}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select(".titleline > a")
    subtext = soup.select(".subtext")
    return links, subtext

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get("href", None)
        vote = subtext[idx].select(".score")
        if vote:
            points = int(vote[0].getText().replace(" points", ""))
            if points > 99:
                hn.append({"title": title, "link": href, "votes": points})
    return hn

# Loop through multiple pages
all_stories = []
for page in range(1, 10):  # Scrape pages 1 to 3
    links, subtext = fetch_hn_page(page)
    page_stories = create_custom_hn(links, subtext)
    all_stories.extend(page_stories)

# Sort & display all results
sorted_stories = sort_stories_by_votes(all_stories)
pprint.pprint(sorted_stories)