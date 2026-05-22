class Employee:

    def __init__(
            self,
            name:str,
            salary:int,
            skills:list[str]
        ):
        
            self.name=name
            self.salary=salary
            self.skills=skills

    def introduce(self):
        print(f"My name is {self.name}")

    def is_high_paid(self):
        if self.salary > 5000:
            return True
        
        return False
    
    def show_skills(self):
        for skill in self.skills:
            print(f"- {skill}")


employee= Employee(
    "Mateen",
    6000,
    ["Python","AI"]
    )

employee.introduce()
print(employee.is_high_paid())
employee.show_skills()
