from flask import Flask, render_template, redirect, request, url_for, send_from_directory, jsonify
from serviceNow import submit, upload, update, iterateList, updateReward, getData
from CallAuth import getAuthCode, getIDToken, getUserEmail, getUserNetID, decodeToken
from Authentication import authenticate, authenticateAdmin, authenticateUser
import os

from werkzeug.utils import secure_filename
import sched, time
import atexit
from apscheduler.scheduler import Scheduler
import requests
from sqlite import user_isAdmin, update_reward, get_user_name, get_user_reward, get_user_types, get_user_submissions, top5users, update_types, submissions_addone, insert_user, is_user_in_db, all_users, removeResolvedTicket

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 26214400
afterPost = False
userAfterPost = False
netID = ""
admins = {"nbk5", "yk200","bc204", "jnh28", "nb89"}

cron = Scheduler(daemon=True)
cron.start()

@cron.interval_schedule(seconds=10) #can change this to once or twice every week
def job_function():
    update()

@app.route('/', methods=['GET', 'POST'])
def loading_page():
    return render_template('loadingPage.html')

@app.route("/submission", methods=["POST", "GET"])
def submit_page():
    if request.method == "POST":
       Submission_URL = request.form["Submission_URL"]
       id_token = getIDToken(authenticate(getAuthCode(Submission_URL)))
       decoded = decodeToken(id_token)
       email = getUserEmail(decoded)
       netID = getUserNetID(decoded)
       print("User's email: " + email)
       print("User's netID: " + netID)
       name = request.form["name"]
       vcm = request.form["vcm"]
       domain = request.form.get("domain")
       vuln = request.form.get("vuln")
       reproduce = request.form["reproduce"]
       description = request.form["descrip"]
       impact = request.form["impact"]
       fixes = request.form["fixes"]
       uploads ={'one':request.files['attachmentOne'],'two':request.files['attachmentTwo'],'three':request.files['attachmentThree'],'four':request.files['attachmentFour'],'five':request.files['attachmentFive']}
       for attachment in uploads:
           if uploads[attachment].filename != '':
               if ' ' in uploads[attachment].filename:
                   uploads[attachment].filename = uploads[attachment].replace(' ','')
               if '(' in uploads[attachment].filename:
                   uploads[attachment].filename = uploads[attachment].replace('(','')
               if ')' in uploads[attachment].filename:
                   uploads[attachment].filename = uploads[attachment].filename.replace(')','')
               uploads[attachment].save(os.path.join(app.instance_path, 'uploads', secure_filename(uploads[attachment].filename)))
       submit(name,vcm,domain,vuln,reproduce,description,impact,fixes,uploads,netID)
       if not is_user_in_db(netID):
           insert_user(netID,name,0,0,0, None)
       return render_template("endPage.html") 
    else:
        return render_template("submission.html")

@app.route('/rewards', methods=['GET', 'POST'])
def rewards_page():
    return render_template('rewards.html')

@app.route('/admin-rewards', methods=['GET', 'POST'])
def admin_rewards_page():
    if user_isAdmin(netID):
        return render_template('rewardsAdmin.html')
    return render_template('errorPage.html')

@app.route('/howtoplay', methods=['GET', 'POST'])
def htp_page():
    return render_template('htp.html')

@app.route('/admin-howtoplay', methods=['GET', 'POST'])
def admin_htp_page():
    if user_isAdmin(netID):
        return render_template('htpAdmin.html')
    return render_template('errorPage.html')

@app.route('/FAQ', methods=['GET', 'POST'])
def FAQ_page():
    return render_template('FAQ.html')

@app.route('/end_page', methods=['GET', 'POST'])
def end_page():
    return render_template('endPage.html')

@app.route('/ticket')
def ticket_page():
    if user_isAdmin(netID):
        dict1 = {}
        output = iterateList()
        for i in output:
            dict1[i] = getData(output[i])
        return render_template('ticket.html',output=dict1)
    return render_template('errorPage.html')

@app.route('/ticket-<num>')
def indivTicket(num):
    if user_isAdmin(netID):
        output = getData(iterateList()[int(num)])
        return render_template('indivTicket.html',output=output , num=num)
    return render_template('errorPage.html')


atexit.register(lambda: cron.shutdown(wait=False))

@app.route('/verificationUser', methods=['GET', 'POST'])
def verificationUser_page():
    return render_template('verificationUser.html')

# NOT DONE YET 
@app.route('/userProfile', methods=['GET', 'POST'])
def userProfile():
    global userAfterPost
    while(not userAfterPost):
        if request.method == "POST":
            url = request.json['URL']
            decoded = decodeToken(getIDToken(authenticateUser(getAuthCode(url))))
            global netID
            netID = getUserNetID(decoded)
            userAfterPost = True
            
    if request.method != "POST":
        return render_template("indivProfile.html", netID = netID, reward = get_user_reward(netID), submissions = get_user_submissions(netID), name = get_user_name(netID), types = get_user_types(netID))
    return render_template("errorPage.html")

@app.route('/adminLoading', methods=['GET', 'POST'])
def adminLoading_page():
    afterPost = False
    return render_template('adminLoading.html')

@app.route('/verification', methods=['GET', 'POST'])
def verification_page():
    return render_template('verification.html')

@app.route('/home_page', methods=['GET', 'POST'])
def home_page():
    userAfterPost = False
    leaderboard = top5users()
    return render_template('index.html',leaderboard = leaderboard)

@app.route('/adminIndex', methods=['GET', 'POST'])
def adminindex():
    leaderboard = top5users()
    return render_template('adminIndex.html',leaderboard = leaderboard)

@app.route('/adminPage', methods=['GET', 'POST'])
def authorizeAdmin():
    global afterPost
    while(not afterPost):
        if request.method == "POST":
            url = request.json['URL']
            decoded = decodeToken(getIDToken(authenticateAdmin(getAuthCode(url))))
            global netID
            netID = getUserNetID(decoded)
            afterPost = True
    if request.method != "POST":
        if user_isAdmin(netID):
            leaderboard = top5users()
            return render_template('adminIndex.html',leaderboard = leaderboard)
    return render_template("errorPage.html")

@app.route('/rewardSub-<num>', methods=['GET', 'POST'])
def rewardSub(num):
    if user_isAdmin(netID):
         if request.method == 'POST':
            name = request.form["name"]
            id = request.form["netid"]
            eligible = request.form.get("eligible")
            vuln = request.form.get("vuln")
            domain = request.form.get("domain")
            amount = request.form["amount"]
            update_reward(netID, amount)
            submissions_addone(netID)
            
            update_types(netID, vuln)
            if eligible == "Yes":
                    filler = "is"
            else:
                filler = "is not"
            if amount == '':
                amount = '0'
            notes = request.form["notes"]
            output = {'name':name, 'id': id, 'eligible': eligible, 'domain': domain, 'amount':amount, 'filler': filler, 'vuln': vuln, 'notes':notes}
            updateReward(int(num))
            return render_template("adminEnd.html",output=output)
         else:
            arr = getData(iterateList()[int(num)])
            return render_template("rewardSub.html",output=arr)
    return render_template('errorPage.html')

@app.route('/adminEnd')
def adminEnd():
    return render_template("adminEnd.html",output=output)

@app.route('/userProfiles')
def userProfiles():
    userslist = all_users()
    return render_template("userProfiles.html", userslist = userslist)

@app.route('/userIndivProfile-<i>')
def indivProfile(i):
    name = get_user_name(i)
    submissions = get_user_submissions(i)
    reward = get_user_reward(i)
    types = get_user_types(i)
    return render_template("adminindivProfile.html", netid = i, name = name, submissions = submissions, reward = reward, types = types)

if __name__ == "__main__":
    app.run(debug=True)