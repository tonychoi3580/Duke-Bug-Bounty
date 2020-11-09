
class User:
    def __init__(self, netid, name, isAdmin):
        self.netid = netid
        self.name = name
        self.isAdmin = isAdmin
        self.submissions = submissions
        self.reward = reward
        self.types = types

    @property
    def email(self):
        return "{}@duke.edu".format(self.netid)
    def __repr__(self):
        return "User('{}','{}','{}','{}','{}')".format(self.netid, self.name, self.isAdmin, self.submissions, self.reward, self.types)

class Unresolved_Tickets:
    def __init__(self, sysid):
        self.sysid = sysid

class Resolved_Tickets:
    def __init__(self, sysid):
        self.sysid = sysid