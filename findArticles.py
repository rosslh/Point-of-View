__all__ = ['search']

import datetime
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

# Cookie jar. Stored at the user's home folder.
# home_folder = os.getenv('HOME')
# if not home_folder:
#     home_folder = os.getenv('USERHOME')
#     if not home_folder:
#         home_folder = '.'   # Use the current folder on error.
# cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
# try:
#     cookie_jar.load()
# except Exception:
#     pass


def get_page(url):

    if(sys.platform == "linux"):
        browser = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    else:
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
                recordSearch(url)  # record the search page
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


def getResults(keyword, start_timestamp, stop_timestamp, step_days):
    # CNN
    cnn_url = "www.cnn.com"
    while start_timestamp <= stop_timestamp:
        start = datetime.datetime.fromtimestamp(start_timestamp).strftime('%m/%d/%Y')
        end = datetime.datetime.fromtimestamp(start_timestamp + step_days * 86400).strftime('%m/%d/%Y')
        for a in search("{} url:{}".format(keyword, cnn_url), stop=9, startdate=start, enddate=end):
            recordUrl(a)
            date = (start_timestamp + stop_timestamp) // 2
            recordDate(date)
    # FOX
    fox_url = "www.foxnews.com"
    while start_timestamp <= stop_timestamp:
        start = datetime.datetime.fromtimestamp(start_timestamp).strftime('%m/%d/%Y')
        end = datetime.datetime.fromtimestamp(start_timestamp + step_days * 86400).strftime('%m/%d/%Y')
        for a in search("{} url:{}".format(keyword, fox_url), stop=9, startdate=start, enddate=end):
            recordUrl(a)
            date = (start_timestamp + stop_timestamp) // 2
            recordDate(date)


def recordSearch(query):
    with open("searches.txt", "a") as f:
        f.write(query)


def recordUrl(url):
    with open("articles.txt", "a") as f:
        f.write(url)


def recordDate(date):
    with open("dates.txt", "a") as f:
        f.write(date)


getResults("Trump", 1454515366, 1486137766, 7)
