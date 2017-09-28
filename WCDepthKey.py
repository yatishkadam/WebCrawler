import requests
from bs4 import BeautifulSoup
import re
import time

main_links=[]


'''implementation of DFS algorithm'''
def dfs_links(url, depth, key):
    if len(main_links) > 1000:
        return
    if depth > 5:
        return
    if url in main_links:
        return
    main_links.append(url)

    links = linkcrawler(url, key)
    for i in links:
        dfs_links(i, depth + 1, key)
    return True


''' Function to extract url
    given the url
    returns a list with the extracted urls
'''
def linkcrawler(url,key):
    a, b = [], []
    s=' '
    time.sleep(1)
    source = requests.get(url)
    plain_text = source.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    data = soup.find('div', {'class': 'mw-body-content'})
    if len(soup.find('ol', class_='references') or ()) > 1:
        soup.find('ol', class_='references').decompose()
    wiki="https://en.wikipedia.org"
    # extracting the links using the regular expression
    for link in data.find_all('a', {'href': re.compile("^/wiki")}):
        if ':' not in link.get('href'):
            try:
                s = str(link.text)
            except UnicodeEncodeError as e:
                error = e

            if (key.lower() in str(link.get('href')).lower()) or (key.lower() in s.lower()):
                href = wiki + link.get('href')
                hlist = href.split('#')
                a.append(str(hlist[0]))
    remove_duplicates(a, b)
    return b

#funtion to remove the duplicates in the lists provided
def remove_duplicates(a, b):
    for i in a:
        if i not in b:
            if len(i) > 1:
                    b.append(i)
    return b

#funtion to write the extratced links to a file
def write_to_file():
    numbering = 1
    file = open('task2b_urls.txt', 'w+')
    for link in main_links:
        print_links = str(numbering) + " " + str(link) + "\n"
        file.write(print_links)
        numbering += 1
    file.close()
#main function
def crawler(seed,key):
    dfs_links(seed, 1 , key)
    write_to_file()

crawler("https://en.wikipedia.org/wiki/Sustainable_energy","solar")
