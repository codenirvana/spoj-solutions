import requests
from bs4 import BeautifulSoup
import grequests


USERNAME = ""
PASSWORD = ""

BASE_URL = "http://www.spoj.com"
LOGIN_URL = "/login/"
URL = "/status/"+USERNAME+"/all/"

def saveCode(results):
    for result in results:
        html = result.text
        soup = BeautifulSoup(html, "html.parser")

        problemcode = soup.find("input", {"name":"problemcode"})
        languageId = soup.find('option', {'selected': True}).get('value')

        textarea = '<textarea rows="20" cols="70" name="file" id="file" style="width: 100%;" data-input-file="1">'
        for item in html.split("</textarea>"):
            if textarea in item:
                code = item[ item.find(textarea)+len(textarea) : ]

def main():
    session = requests.session()

    payload = {
        "login_user": USERNAME,
        "password": PASSWORD
    }
    print('Logging in...')
    result = session.post(BASE_URL + LOGIN_URL, data = payload)
    print('Success!')

    result = session.get(BASE_URL + URL)
    soup = BeautifulSoup(result.text, "html.parser")
    user = soup.find('a', href="/users/uvasu").text.strip()
    user = user[:len(user)-1]
    print('Hello ' + user)

    solutions = dict()

    while 1:
        rows = soup.select('.kol1 .statusres .small')
        rows_found = len( rows )

        for row in rows:
            sol = row.find('a').get('href')
            key = sol.split("/")[2]
            if key in solutions:
                continue
            solutions[key] = sol

        nextPage = soup.select('.pagination li')[-2].find('a')
        if(nextPage):
            print('Next Page...')
            result = session.get(BASE_URL + nextPage.get('href'))
            soup = BeautifulSoup(result.text, "html.parser")
        else:
            break


    print('Fetching urls...')
    urls = list(solutions.values())
    unsent_request = (grequests.get(BASE_URL + url, session=session) for url in urls)
    results = grequests.map(unsent_request)

    saveCode(results)


if __name__ == '__main__':
    main()
