import os
import getpass
import requests
import grequests
from bs4 import BeautifulSoup

session = requests.session()

BASE_URL = "http://www.spoj.com"

# find/create valid path
def basePath():
    while 1:
        path = input('Enter path to save files: ').strip()
        # complete home path
        if(path.startswith('~/')):
            path = path.replace( '~', os.path.expanduser('~'), 1  )

        # create path if not exists
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


# save source code files
def createFiles(results, problemCode):
    path = basePath()   # path to save files
    print('Writing files...')
    total = len(results)
    for i in range( total ):
        extension = results[i].headers['Content-Disposition'].split('-src')[1]
        sourceFile = open(path + problemCode[i] + extension, "w")
        sourceFile.write(results[i].text)
        sourceFile.close()

    print( 'Total files saved: ' + str(total) )


# fetch all submissions
def process(soup):
    problemCode = []
    problemUrl = []

    while 1:
        rows = soup.select('.kol1 .statustext a.sourcelink')    # AC submissions

        for row in rows:
            code = row.get('data-pcode')
            if(code in problemCode):
                continue    # skip repeat submissions for same problem
            problemCode.append(code)    # append problem code

            # build source code url, /files/src/save/:ID
            url = row.get('data-url').split('/')
            url.insert(3, 'save')
            url = '/'.join( url )
            problemUrl.append(url)  # append problem url

        # check for next page
        nextPage = soup.select('.pagination li')[-2].find('a')
        if(nextPage):
            print('Searching submissions...')
            result = session.get(BASE_URL + nextPage.get('href'))
            soup = BeautifulSoup(result.text, "html.parser")
        else:
            break

    # fetch all problemUrl
    print('Fetching source code...')
    unsent_request = (grequests.get(BASE_URL + url, session=session) for url in problemUrl)
    results = grequests.map(unsent_request)

    createFiles(results, problemCode)


def main():
    USERNAME = input('Username: ')
    PASSWORD = getpass.getpass('Password: ')

    payload = {
        "login_user": USERNAME,
        "password": PASSWORD
    }

    print('Logging in...')
    result = session.post(BASE_URL + "/login/", data=payload)

    # fetch user submissions page
    result = session.get(BASE_URL + "/status/" + USERNAME + "/all/")

    soup = BeautifulSoup(result.text, "html.parser")

    # successfully logged in, if logout button found
    logout_btn = soup.find("a", {"href": "/logout"})
    if not logout_btn:
        print('Failed!')
        return

    # get user real name
    user = soup.find('a', href="/users/" + USERNAME).text.strip()[:-1]
    print('Hello ' + user)

    process(soup)


if __name__ == '__main__':
    main()
