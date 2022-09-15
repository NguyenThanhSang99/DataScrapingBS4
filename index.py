import sys, getopt
import os
from time import sleep
from bs4 import BeautifulSoup
import requests

def writeFileTxt(fileName, content):
    with open(fileName, 'a', encoding="utf-8") as f1:
        f1.write(content + os.linesep)

def getInformation(search_key, number_of_pages = 2):
    try:
        url="https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" + search_key

        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(url).text

        # Parse the html content
        soup = BeautifulSoup(html_content, "lxml")

        # Find element which have href attr
        link_list = soup.find_all("a", class_="api_txt_lines total_tit _cross_trigger")
        links = [link['href'] for link in link_list]

        count = 1

        for link in links:
            print(link)
            food_page = requests.get(link).text
            print(food_page)
            food_soup = BeautifulSoup(food_page, "lxml")
            data = food_soup.find_all("span", class_="se-fs- se-ff-   ")
            print(data)
            if (count == number_of_pages): 
                break
            count += 1
        
    except Exception as e:
        print("Error: ", e)

def main(argv):
    pageName = ''
    totalPost = 0
    try:
        opts, args = getopt.getopt(argv,"hs:n:",["skey=","npage="])
    except getopt.GetoptError:
        print('python index.py -s <search> -n <number of pages>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python index.py -s <search key> -n <number of pages>')
            sys.exit()
        elif opt in ("-s", "--skey"):
            search_key = arg
        elif opt in ("-n", "--npage"):
            number_pages = int(arg)

    print("Search key: ", search_key)

    getInformation(search_key, number_pages)


if __name__ == "__main__":
   main(sys.argv[1:])