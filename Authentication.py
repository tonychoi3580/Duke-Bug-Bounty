import requests, json
import subprocess
import sys 
import http.client


# sends a post request to duke oauth using the authorization code from sumbission page url and bug bounty credentials
# returns string containing access token, id token, scope, expiration, token_type
def authenticate(authCode):

    token_url = "https://oauth.oit.duke.edu/oidc/token"

    headers = {'content-type': "application/x-www-form-urlencoded"}

    payload = "grant_type=authorization_code&client_id=bugbounty_dev&client_secret=ALmmRgvgtd8GM780MKw6dQVdLakSwuRASNUCDmdrL9oGEJzx8yAlrX7k2CEtjCKgid01LHXOj9m_USlOEjCPq3U&code="+authCode+"&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fsubmission"

    r = requests.post(token_url, data=payload, headers=headers)

    ret = r.text

    return ret

def authenticateAdmin(authCode):

    token_url = "https://oauth.oit.duke.edu/oidc/token"

    headers = {'content-type': "application/x-www-form-urlencoded"}

    payload = "grant_type=authorization_code&client_id=bugbounty_dev&client_secret=ALmmRgvgtd8GM780MKw6dQVdLakSwuRASNUCDmdrL9oGEJzx8yAlrX7k2CEtjCKgid01LHXOj9m_USlOEjCPq3U&code="+authCode+"&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fverification"

    r = requests.post(token_url, data=payload, headers=headers)

    ret = r.text

    return ret

def authenticateUser(authCode):

    token_url = "https://oauth.oit.duke.edu/oidc/token"

    headers = {'content-type': "application/x-www-form-urlencoded"}

    payload = "grant_type=authorization_code&client_id=bugbounty_dev&client_secret=ALmmRgvgtd8GM780MKw6dQVdLakSwuRASNUCDmdrL9oGEJzx8yAlrX7k2CEtjCKgid01LHXOj9m_USlOEjCPq3U&code="+authCode+"&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2FverificationUser"

    r = requests.post(token_url, data=payload, headers=headers)

    ret = r.text

    return ret

    # conn = http.client.HTTPSConnection("")

    #payload = "grant_type=authorization_code&client_id=bugbounty_dev&client_secret=ALmmRgvgtd8GM780MKw6dQVdLakSwuRASNUCDmdrL9oGEJzx8yAlrX7k2CEtjCKgid01LHXOj9m_USlOEjCPq3U&code="+authCode+"&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fsubmission"

    # headers = {'content-type': "application/x-www-form-urlencoded"}

    # conn.request("POST", "https://oauth.oit.duke.edu/oidc/token", headers)

    # res = conn.getresponse()
    # data = res.read()

    # print (data.decode("utf-8"))
    # return

# authorize_url = ""
# token_url = ""
# callback_uri = "http://localhost:5000/submission"


# curl -ik -X POST https://oauth.oit.duke.edu/oidc/token \
# -d grant_type=authorization_code \
# -d code=QSHg6h \
# -d redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fsubmission \
# -d client_id=bugbounty_dev \
# -d client_secret=ALmmRgvgtd8GM780MKw6dQVdLakSwuRASNUCDmdrL9oGEJzx8yAlrX7k2CEtjCKgid01LHXOj9m_USlOEjCPq3U \

# curl linktotheapi.com -H
