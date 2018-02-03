import urllib.request
import re

def scrapeArticle(articleURL):
    fp = urllib.request.urlopen(articleURL)
    mybytes = fp.read()

    articleString = mybytes.decode("utf8")
    fp.close()


    paragraphClassIndices = [match.start() for match in re.finditer(re.escape("zn-body__paragraph"), articleString)]

    unfilteredSubstrings = []
    filteredSubstrings = []

    for index in paragraphClassIndices:
        substring = articleString[index:]
        startIndex = substring.index(">")
        endIndex = substring.index("</div>")
        unfilteredSubstrings.append(substring[startIndex+1:endIndex])

    for string in unfilteredSubstrings:
        while string.find("<") != -1:
            startIndex = string.find("<")
            endIndex = string.find(">")
            string = (string[:startIndex] + string[endIndex + 1:])

        filteredSubstrings.append(string)

    print("\n".join(filteredSubstrings))

    return filteredSubstrings