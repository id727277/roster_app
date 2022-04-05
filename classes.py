

class Concierge:
    """ General concierge class"""

    num_of_concierges = 0 # total amount of employees

    def __init__(self, first, last, user_id, phone, tg_account, dept, remote):

        self.first = first
        self.last = last
        self.user_id = user_id
        self.phone = phone
        self.tg_account = tg_account
        self.dept = dept
        self.remote = remote

        Concierge.num_of_concierges += 1
    
    
    def __repr__(self):
        return f"Concierge('{self.first}', '{self.last}', '{self.user_id}', '{self.phone}', '{self.tg_account}', '{self.dept}', '{self.remote}')"
        
    def __str__(self):
        return f"{self.first} {self.last} - {self.dept}"
    

class Remote(Concierge):
    pass

class Induction(Concierge):
    pass

class Supervisor(Concierge):
    pass

class Quality(Concierge):
    pass

class Learning(Concierge):
    pass

class Administration(Concierge):
    pass
