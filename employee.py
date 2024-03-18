from db import c, conn


class Employee(object):
    def __init__(self, name, surname, age, pk=None):
        self.id = pk
        self.name = name
        self.surname = surname
        self.age = age

    @classmethod
    def get(cls, pk):
        result = c.execute("SELECT * FROM employee WHERE id = ?", (pk,))
        values = result.fetchone()
        if values is None:
            return None
        employee = Employee(values["name"], values["surname"], values["age"], values["id"])
        return employee

    @classmethod
    def get_list(cls, **filters):
        conditions = []
        params = []
        for key, value in filters.items():
            if value is not None:
                conditions.append(f"{key} = ?")
                params.append(value)

        if conditions:
            condition_str = " AND ".join(conditions)
            result = c.execute(f"SELECT * FROM employee WHERE {condition_str}", params)
        else:
            result = c.execute("SELECT * FROM employee")

        employees = []
        for values in result:
            employee = cls(values["name"], values["surname"], values["age"], values["id"])
            employees.append(employee)
        return employees

    def __repr__(self):
        return "<Employee {}>".format(self.name)

    def update(self):
        c.execute("UPDATE employee SET name = ?, surname = ?, age = ? WHERE id = ?",
                  (self.name, self.surname, self.age, self.id))

    def create(self):
        c.execute("INSERT INTO employee (name, surname, age) VALUES (?, ?, ?)", (self.name, self.surname, self.age))
        self.id = c.lastrowid

    def save(self):
        if self.id is not None:
            self.update()
        else:
            self.create()
        return self

    def delete(self):
        c.execute("DELETE FROM employee WHERE id = ?", (self.id,))
        conn.commit()

    def __lt__(self, other):
        return self.age < other.age
