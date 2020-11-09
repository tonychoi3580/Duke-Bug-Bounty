from flask import Flask, redirect, request

import requests, json
import subprocess
import sys 
import http.client

def authenticate(authCode):

    conn = http.client.HTTPSConnection("")

    authCode = "abcd"

    payload = "grant_type=authorization_code&client_id=bugbounty_dev&client_secret=ALmmRgvgtd8GM780MKw6dQVdLakSwuRASNUCDmdrL9oGEJzx8yAlrX7k2CEtjCKgid01LHXOj9m_USlOEjCPq3U&code="+authCode+"&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fsubmission"

    headers = {'content-type': "application/x-www-form-urlencoded"}

    conn.request("POST", "https://oauth.oit.duke.edu/oidc/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

# authorize_url = ""
# token_url = ""
# callback_uri = "http://localhost:5000/submission"


# curl -ik -X POST https://oauth.oit.duke.edu/oidc/token \
# -d grant_type=authorization_code \
# -d code=pVRDyb \
# -d redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fsubmission \
# -d client_id=bugbounty_dev \
# -d client_secret=ALmmRgvgtd8GM780MKw6dQVdLakSwuRASNUCDmdrL9oGEJzx8yAlrX7k2CEtjCKgid01LHXOj9m_USlOEjCPq3U \
