#Need to install requests package for python
#easy_install requests
import requests
import pprint
import json
import imghdr
import magic
import os
from collections import deque
from sqlite import addResolvedTicket, addUnresolvedTicket, submissions_addone, addRewardedTicket, getSysid, getSysidResolved, removeUnresolvedTicket, removeResolvedTicket

def submit(name,vcm,domain,vuln,reproduce,description,impact,fixes,uploads,netID):
    
    # Set the request parameters
    url = 'https://dukesandbox.service-now.com/api/now/table/incident'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'api.bugBounty.oit'
    pwd = 'L8v7*0r@Vr*qDUuC^FqjBA2oq7V34hzcGtBde$xm'
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"caller_id\":\"Joe User\",\"u_service_provider\":\"Duke University\",\"u_it_service\":\"Bug Bounty\",\"service_offering\":\"Bug Bounty Submission\",\"impact\":\"Workgroup\",\"urgency\":\"2 - Medium\",\"priority\":\"3 - Moderate\",\"contact_type\":\"Event\",\"incident_state\":\"Active\",\"assignment_group\":\"Security-University\",\"short_description\":\"Bug Bounty: "+vuln+' vulnerability found on '+domain+"\",\"description\":\"User: "+name+"\\nnetID: "+netID+"\\nVCM: "+vcm+"\\nVulnerability: "+vuln+"\\nDomain: "+domain+"\\nDescription: "+description+"\\nImpact: "+impact+"\\nReproduction Method: "+reproduce+"\\nProposed Solution: "+fixes+"\"}")
    
    # Get the sysID
    sys_id = response.json()['result']['sys_id']
    addUnresolvedTicket(sys_id)
    
    for attachment in uploads:
        if uploads[attachment].filename != '':
            upload(sys_id,uploads[attachment])
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        return

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)

def upload(sys_id,attachment):
    url = 'https://dukesandbox.service-now.com/api/now/attachment/upload'

    # Specify Parameters for File Being Uploaded, the table_name and table_sys_id should be replaced with values that make
    # sense for your use case
    payload = {'table_name':'incident', 'table_sys_id': sys_id}

    # Get the file type
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'instance/uploads/')
    attach = magic.from_file(my_file+attachment.filename, mime=True)

    # Specify Files To Send and Content Type. When specifying fles to send make sure you specify the path to the file, in
    # this example the file was located in the same directory as the python script being executed.
    # it is important to specify the correct file type
    files = {'file': (attachment.filename, open(my_file+attachment.filename, 'rb'), attach, {'Expires': '0'})}

    # Eg. User name="username", Password="password" for this code sample. This will be sent across as basic authentication
    user = 'api.bugBounty.oit'
    pwd = 'L8v7*0r@Vr*qDUuC^FqjBA2oq7V34hzcGtBde$xm'

    # Set proper headers
    headers = {"Accept":"*/*"}

    # Send the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers, files=files, data=payload)

    # Check for HTTP codes other than 201
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Print Resopnse Details
    print('Response Status Code:', response.status_code)

    print('')
    print('Reponse Payload:')
    print(json.dumps(response.json(), indent=4))

def getData(sys_id):
    # Set the request parameters
    url = 'https://dukesandbox.service-now.com/api/now/table/incident/'+sys_id

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'api.bugBounty.oit'
    pwd = 'L8v7*0r@Vr*qDUuC^FqjBA2oq7V34hzcGtBde$xm'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        #print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    description = response.json()['result']['description']
    openedAt = response.json()['result']['opened_at']
    resolvedAt = response.json()['result']['resolved_at']
    notes = response.json()['result']['u_last_work_note']
    if notes != '':
        notes = notes.split('(Work notes)\n')[1]
    incident = response.json()['result']['number']
    info = description.split('\n')
    name = info[0].split(': ')[1]
    netID = info[1].split(': ')[1]
    vulnerability = info[3].split(': ')[1]
    domain = info[4].split(': ')[1]
    descrip = info[5].split(': ')[1]
    impact = info[6].split(': ')[1]
    state = response.json()['result']['state']  #indicates if ticket is resolved
    arr = {'name':name, 'vulnerability':vulnerability, 'state': state, 'openedAt':openedAt, 'resolvedAt': resolvedAt, 'domain':domain, 'netID': netID, 'incident': incident, 'notes': notes, 'descrip':descrip, 'sys_id':sys_id}
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    #print(data)
    return arr

def update(): 
    lines = getSysid()
    for sys_id in lines:
        if getData(sys_id)['state'] == '6':
            addResolvedTicket(sys_id)
            removeUnresolvedTicket(sys_id)
            
    

def iterateList():
    idlist = getSysidResolved()
    output = {}
    for i in range(len(idlist)):
        output[i]= idlist[i]
    return output

def updateReward(num):
    sys_id = iterateList()[num]
    removeResolvedTicket(sys_id)
    addRewardedTicket(sys_id)

print(getSysidResolved())
