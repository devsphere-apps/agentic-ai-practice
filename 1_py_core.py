# variables and data types
name = "Abdul Mateen"
age = 29
height = 5.9
is_analyst = True
skills= ["Python","SOC","AI"]
person= {"name":"Mateen","age":29,"city":"Peshawar"}
users = {
    "name":"Mateen",
    "age":29,
    "is_admin":True,
    "skills":["Python","SOC","AI"],
    "address":{
        "city":"Peshawar",
        "country":"Pakistan"
    },
    "salary":5000,
    "experience":6
}

employees = [
    {
        "name":"Mateen",
        "skills":["Python","AI"]
    },
    {
        "name":"Kaleem",
        "skills":["SOC","Networking"]
    }
]

severity = "medium"

numbers = [1,2,3,4,5,6,7,8]
alerts = ["brute_force", "port_scan", "sql_injection", "ddos"]

nothing = None

# def greet(na:str)->str:
#     return f"Hello, {na}"

# def greet_with_default_params(name:str, age:int =20)->str:
#     return f"Hello {name}, your age is {age}"

# def get_info(person:dict)->tuple[str,int,str]:
#     name = person["name"]
#     age = person["age"]
#     city = person['city']

#     return name, age,city


# person_name,person_age, person_city = get_info(person)

# print(greet(name))
# print(greet_with_default_params(name))
# print(person_name)
# print(person_age)
# print(person_city)


# if severity == "critical":
#     print("Page: On Call")
# elif severity == "high":
#     print("Create Ticke")
# elif severity == "medium":
#     print("Log and monitor")
# else:
#     print("Chil mode take a coffee and enjoy")

# ternary one liner 
# action = "page" if severity == "medium" else "log"
# print(f"Action {action}")

# if "SOC" in skills:
#     print("SOC skill found!")

# if "age" in person:
#     print(f"Age is: {person["age"]}")

# print(user["name"])
# print(user['addresss']["city"])
# print(user["skills"][0])

# if user['is_admin']:
#     print("User is Admin")
# else:
#     print("user is not admin")

# if user["addresss"]["country"] == "Pakistan":
#     print("Pakistani user")

# if user["age"] > 18 and user["is_admin"]:
#     print("Adult admin user")

# if user["salary"] > 4000 and user["experience"] > 3:
#     print("Senior Engineer")

# loops
# for skill in skills:
#     print(skill)

# for i in range(3):
#     print(i)

# for i , skill in enumerate(skills):
#     print(f"{i} : {skill}")

# for key, value in person.items():
#     print(f"{key}: {value}")

# count = 0

# while count < 3:
#     print(f"Count: {count}")
#     count+=1


# for skill in skills:
#     print(skill)

# for index, skill in enumerate(skills):
#     print(index,skill)

# for key, skill in person.items():
#     print(f"{key}: {skill}")

# for employee in employees:
#     print(employee["name"])

#     for skill in employee["skills"]:
#         print(f" - {skill}")

# for num in numbers:
#     if num % 2 == 0:
#         print(num, "is even")

#     else:
#         print(num, "is odd")

# for num in range(10):
#     if num == 2:
#         continue
#     print(num)


# for key, user in users.items():

#    if type(user) == dict:
#     print(user["country"])

# for key,alert in enumerate(alerts):
#     print(f"{key}: {alert}")

# for alert in alerts:

#     if "s" in alert:
#         print(alert)