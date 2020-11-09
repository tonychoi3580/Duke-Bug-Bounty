from flask import Flask, render_template, redirect, request, url_for, send_from_directory, jsonify
from serviceNow import submit, upload, update
from CallAuth import getAuthCode, getIDToken, getUserEmail, getUserNetID, decodeToken
from Authentication import authenticate
import os
from serviceNow import submit, upload
from werkzeug.utils import secure_filename
import sched, time
import atexit
from apscheduler.scheduler import Scheduler

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 26214400

global admins
admins = {"nbk5"}

@app.route('/adminLoading', methods=['GET', 'POST'])
def loading_page():
    return render_template('adminLoading.html')

@app.route('/adminPage', methods=['GET', 'POST'])
def authorizeAdmin():
    loginURL = request.POST['serverResponse']  # get the redirected page url to go here 
    decoded = decodeToken(getIDToken(authenticate(getAuthCode(loginURL))))
    global netID
    netID = getUserNetID(decoded)
    if netID in admins:
        return render_template('adminPage.html')
    else:
        return render_template('errorPage.html')

# @app.route('/adminPage', methods=['GET', 'POST'])
# def adminPage():
#     if database.get(netID) == True:
#         return render_template('adminPage.html')
#     else:
#         return render_template('errorPage.html')


if __name__ == "__main__":
    app.run(debug=True)
