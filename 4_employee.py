class Employee:
    def __init__(self,name:str,salary:int,department:str):
        self.name= name
        self.salary=salary
        self.department=department
    
    def introduce(self):
        print(f"{self.name} working in {self.department} department")

    def is_highly_paid(self):
        return self.salary > 3000

class Company:

    def __init__(self,company_name:str):
        self.company_name = company_name
        self.employees=[]
    
    def add_employee(self,employee:Employee):
        self.employees.append(employee)

    def show_all_employees(self):
        for emp in self.employees:
            emp.introduce()
    
    def show_high_paid_employees(self):
        for emp in self.employees:
            if emp.is_highly_paid():
                print(
                    f"{emp.name} earns {emp.salary}"
                )
        


emp1 = Employee(
    "Mateen",
    5000,
    "AI"
);
emp2 = Employee(
    "Kaleem",
    3000,
    "Cyber Security"
)
emp3 = Employee(
    "Saleem",
    7000,
    "Marketing"
)

comp = Company("OpenAI Pakistan")
comp.add_employee(emp1)
comp.add_employee(emp2)
comp.add_employee(emp3)

print(f"\nAll Employees:")
comp.show_all_employees()

print("\nHigh Paid Employees:")
comp.show_high_paid_employees()