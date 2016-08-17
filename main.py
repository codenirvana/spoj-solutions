import os
import  getpass
import requests
import grequests
from bs4 import BeautifulSoup

session = requests.session()

BASE_URL = "http://www.spoj.com"

def basePath():
    while 1:
        path = input('Enter path to save files: ').strip()

        if(path.startswith('~/')):
            path = path.replace( '~', os.path.expanduser('~'), 1  )

        if not os.path.exists(path):
            print('Path not exists: ' + path)
            permission = input('Do you want to create this path? (Y/N) ')
            if(permission.upper() == 'Y'):
                os.makedirs(path)
            else:
                continue

        print('Valid Path: ' + path)
        permission = input('Save files to this path? (Y/N) ')
        if(permission.upper() == 'Y'):
            break
        else:
            continue
    return path + '/'

def createFiles(results, problemCode):
    path = basePath()
    print('Writing files...')
    total = len(results)
    for i in range( total ):
        extension = results[i].headers['Content-Disposition'].split('-src')[1]
        sourceFile = open(path + problemCode[i] + extension, "w")
        sourceFile.write(results[i].text)
        sourceFile.close()

    print( 'Total files saved: ' + str(total) )

def process(soup):
    problemCode = []
    problemUrl = []

    while 1:
        rows = soup.select('.kol1 .statustext a.sourcelink')

        for row in rows:
            code = row.get('data-pcode')
            if(code in problemCode):
                continue
            problemCode.append(code)
            url = row.get('data-url').split('/')
            url.insert(3, 'save')
            url = '/'.join( url )
            problemUrl.append(url)

        nextPage = soup.select('.pagination li')[-2].find('a')
        if(nextPage):
            print('Searching submissions...')
            result = session.get(BASE_URL + nextPage.get('href'))
            soup = BeautifulSoup(result.text, "html.parser")
        else:
            break

    print('Fetching source code...')
    unsent_request = (grequests.get(BASE_URL + url, session=session) for url in problemUrl)
    results = grequests.map(unsent_request)

    createFiles(results, problemCode)

def main():
    USERNAME = input('User Name: ')
    PASSWORD = getpass.getpass('Password: ')
    URL = "/status/" + USERNAME + "/all/"

    print('Logging in...')

    payload = {
        "login_user": USERNAME,
        "password": PASSWORD
    }
    result = session.post(BASE_URL + "/login/", data=payload)

    result = session.get(BASE_URL + URL)

    soup = BeautifulSoup(result.text, "html.parser")

    logout_btn = soup.find("a", {"href": "/logout"})

    if not logout_btn:
        print('Failed!')
        return

    user = soup.find('a', href="/users/" + USERNAME).text.strip()[:-1]

    print('Hello ' + user)

    process(soup)

if __name__ == '__main__':
    main()
