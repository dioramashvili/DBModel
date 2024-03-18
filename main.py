from employee import Employee
from db import conn


first_user = Employee.get(1)
if first_user is None:
    first_user = Employee("name", "surname", "age")
    first_user.save()

first_user.name = "Tornike"
first_user.save()
conn.commit()
conn.close()
