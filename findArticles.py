import datetime
import re
import sys
import time

from selenium import webdriver

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus, urlparse, parse_qs
    import urllib.parse
else:
    from urllib import quote_plus
    from urlparse import urlparse, parse_qs
    import urllib.parse
# Try to use BeautifulSoup 4 if available, fall back to 3 otherwise.
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

# URL templates to make Google searches.
url_home = "http://www.google.%(tld)s/"
url_search = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
url_next_page = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
url_search_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"


def get_page(url):
    if(sys.platform == "linux"):  # Ross
        browser = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    else:  # Frodi
        browser = webdriver.Chrome()
    browser.get(url)  # navigate to the page
    html = browser.page_source
    return html


def filter_result(link):
    try:
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link

    # Otherwise, or on error, return None.
    except Exception:
        pass
    return None


def search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=5.0, startdate="", enddate=""):
    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = set()

    # Prepare the search string.
    query = quote_plus(query)

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    if(startdate and enddate):  # also change one down the page
        url += "&" + urllib.parse.urlencode({"tbs": "cdr:1,cd_min:{},cd_max:{}".format(startdate, enddate)})

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    # if url in prevUsedUrls():
    #     return []
    while not stop or start < stop:
        # Sleep between requests.
        time.sleep(pause)
        # Request the Google Search results page.
        html = get_page(url)
        # Parse the response and process every anchored URL.
        soup = BeautifulSoup(html, "lxml")
        try:
            anchors = soup.find(id='search').findAll('a')
            for a in anchors:
                try:
                    link = a['href']
                except KeyError:
                    continue

                # Filter invalid links and links pointing to Google itself.
                link = filter_result(link)
                if not link:
                    continue

                # Discard repeated results.
                h = hash(link)
                if h in hashes:
                    continue
                hashes.add(h)
                # recordSearch(url)  # record the search page

                # Yield the result.
                yield link
        except:
            pass
        # End if there are no more results.
        if not soup.find(id='nav'):
            break

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
        if(startdate and enddate):
            url += "&" + urllib.parse.urlencode({"tbs": "cdr:1,cd_min:{},cd_max:{}".format(startdate, enddate)})


def recordUrl(url, subject):
    with open("./data/{}.txt".format(subject), "a+") as f:
        if url not in f.read().split("\n"):
            f.write("{}\n".format(url))
        else:
            print("Duplicate found: {}".format(url))


def ymdToTimestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "/%Y/%m/%d/").timetuple())


def getDataFromFile(keyword, start, stop):  # [url, date, network, keyword, -2, []]
    out = []
    pattern = re.compile("/20[0-9]{2}/[0-9]{2}/[0-9]{2}/")
    with open("./data/{}.txt".format(keyword), 'r') as f:
        for article in f.read().split("\n"):
            matched = pattern.search(article)
            if matched:
                timestamp = ymdToTimestamp(matched.group(0))
                if start <= timestamp <= stop:
                    out.append([article, timestamp, urlparse(article).netloc, keyword, -2, []])
    return out


def scrapeArticleLinks(keyword, start_timestamp, stop_timestamp, step_days, source1, source2):
    while start_timestamp <= stop_timestamp:
        start = datetime.datetime.fromtimestamp(start_timestamp).strftime('%m/%d/%Y')
        end = datetime.datetime.fromtimestamp(start_timestamp + step_days * 86400).strftime('%m/%d/%Y')
        for a in search("{} site:{}".format(keyword, source1), stop=9, startdate=start, enddate=end):
            recordUrl(a, keyword)
        for a in search("{} site:{}".format(keyword, source2), stop=9, startdate=start, enddate=end):
            recordUrl(a, keyword)
        start_timestamp += step_days * 86400
