class Employee:
    ''' This class will contain general employee attributes and methods
    
    additional general attributes:
    - Sick leave
    - Vacation
    - Training
    '''

    num_of_employees = 0 # total amount of employees

    def __init__(self, first, last, mob_phone, dept):
        self.first = first
        self.last = last
        self.mob_phone = mob_phone
        self.dept = dept

        Employee.num_of_employees += 1
    
    def full_emp_info(self):
        return f"""
Name: {self.first} {self.last}
tel: {self.mob_phone}
dept: {self.dept}
            
            """
    @staticmethod # if you don't need to use instance or class, you can use static methods
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True




class Concierge(Employee):
    
    def __init__(self, first, last, mob_phone, dept, tg_account, workstation, nights=False):
        super().__init__(first, last, mob_phone, dept)
        self.tg_account = tg_account
        self.workstation = workstation
        self.nights = nights

    def full_emp_info(self):
        return super().full_emp_info()




emp1 = Employee('Victor', 'Menkov', 9256969698, 'Dining')
con1 = Concierge('Pavel', 'Testov', 9646547384, 'Events', '@tg_pt', 60305, False)


print(emp1.full_emp_info())
print(con1.full_emp_info())




