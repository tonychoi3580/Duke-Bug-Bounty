import sqlite3
from models import User



conn = sqlite3.connect('bug.db')

c = conn.cursor()

def all_users():
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT netid FROM users")
        newlist = []
        for i in c.fetchall():
            newlist.append(i[0])
        return newlist


def insert_user(netid, name, isAdmin, submissions, reward, types):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (:netid, :name, :isAdmin, :submissions, :reward, :types)", {'netid': netid, 'name': name, 'isAdmin': isAdmin, 'submissions' : submissions, 'reward' : reward, 'types' : types})

def is_user_in_db(netid):
    with sqlite3.connect("bug.db") as conn:
        userlist = all_users()
        if netid in userlist:
            return True
        else:
            return False

def update_reward(netid, reward):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("""UPDATE users SET reward = (SELECT reward FROM users WHERE netid = :netid) + :reward
                    WHERE netid = :netid""",
                  {'netid': netid, 'reward': reward})

def update_types(netid, types):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT types FROM users WHERE netid = :netid",{'netid' : netid})
        asdf = c.fetchall()
        print(len(asdf))
        # if len(asdf) == 0:
        if asdf[0][0]==None:
            c.execute("""UPDATE users SET types = :types || '\n\n'
                    WHERE netid = :netid""",{'netid': netid, 'types': types})
        elif types not in asdf[0][0]:
            c.execute("""UPDATE users SET types = (SELECT types FROM users WHERE netid = :netid) || :types || '\n\n'
                    WHERE netid = :netid""",{'netid': netid, 'types': types})
       

def update_isAdmin(netid, isAdmin):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("""UPDATE users SET isAdmin = :isAdmin
                    WHERE netid = :netid""",
                  {'netid': netid, 'isAdmin': isAdmin})

def submissions_addone(netid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("""UPDATE users SET submissions = (SELECT submissions FROM users WHERE netid = :netid) + 1
                    WHERE netid = :netid""",
                  {'netid': netid})

def top5users():
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("""SELECT * FROM users ORDER BY reward DESC;""")
        return c.fetchmany(3)

def get_all_users(netid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE netid = :netid",{'netid': netid})
        return c.fetchall()

def get_user_name(netid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE netid = :netid",{'netid': netid})
        return c.fetchall()[0][0]

def get_user_types(netid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT types FROM users WHERE netid = :netid",{'netid': netid})
        return c.fetchall()[0][0]


def get_user_submissions(netid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT submissions FROM users where netid = :netid",{'netid': netid})
        return c.fetchall()[0][0]

def get_user_reward(netid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT reward FROM users where netid = :netid",{'netid': netid})
        return c.fetchall()[0][0]


def user_isAdmin(netid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT isAdmin FROM users where netid = :netid",{'netid': netid})
        if c.fetchall()[0][0] == 1:
            return True
        else:
            return False

def addResolvedTicket(sysid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Resolved_Tickets VALUES (:sysid)",{'sysid' : sysid})
    
def addUnresolvedTicket(sysid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Unresolved_Tickets VALUES (:sysid)",{'sysid' : sysid})

def addRewardedTicket(sysid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Rewarded_Tickets VALUES (:sysid)",{'sysid' : sysid})

def removeResolvedTicket(sysid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Resolved_Tickets WHERE sysid = :sysid",{'sysid' : sysid})

def getSysid():
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT sysid FROM Unresolved_Tickets ORDER BY sysid DESC")
        mylist = []
        for i in c.fetchall():
            mylist.append(i[0])
        return mylist

def getSysidResolved():
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("SELECT sysid FROM Resolved_Tickets ORDER BY sysid DESC")
        mylist = []
        for i in c.fetchall():
            mylist.append(i[0])
        return mylist

def removeUnresolvedTicket(sysid):
    with sqlite3.connect("bug.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Unresolved_Tickets WHERE sysid = :sysid",{'sysid' : sysid})
#update_types('bc204','Remote Code Execution')
#c.execute("""CREATE TABLE users (
#            netid text NOT NULL PRIMARY KEY,
#            name text,
#            isAdmin boolean,
#            submissions integer,
#            reward integer,
#)"""
#)
#c.execute("""CREATE TABLE Unresolved_Tickets (
#            sysid text NOT NULL PRIMARY KEY
#)"""
#)
#c.execute("""CREATE TABLE Resolved_Tickets (
#            sysid text NOT NULL PRIMARY KEY
#)"""
#)
#c.execute("""CREATE TABLE Rewarded_Tickets (
#            sysid text NOT NULL PRIMARY KEY
#)"""
#)
#conn.commit()
#c.execute("""ALTER TABLE users
#            ADD COLUMN types text;""")
#c.execute("INSERT INTO users VALUES ('bc204','Tony Choi',True,2,341,null)")
#update_isAdmin('bc204', True)
#c.execute("DROP TABLE users;")
#update_reward('bc204', 15)
#insert_user()
#c.execute("SElECT * FROM users")
#c.execute("""DELETE FROM users WHERE netid = 'bc204';""")
#c.execute("""DELETE FROM users WHERE netid = 'yk200';""")
#c.execute("""DELETE FROM Rewarded_Tickets;""")

#thing = c.fetchall()
#ar = [[str(item) for item in results] for results in thing]
#insert_user('yk200','Yvonne Kuo', 1,0,0,None)
#insert_user('bc204','Tony Choi', 1,0,0,None)
#conn.commit()
print(all_users())
conn.close()
