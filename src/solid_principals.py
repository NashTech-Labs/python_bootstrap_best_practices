
from typing import List

class Employee:
   def __init__(self, name: str, role: str):
       self.name = name
       self.role = role

class Company:
   def __init__(self, employees: List[Employee] = []):
       self._employees = employees

   def add_employee(self, employee: Employee):
       self._employees.append(employee)

   def list_employees(self):
       for employee in self._employees:
           print(f"{employee.name} - {employee.role}")

class ITDepartment(Company):
   def list_employees(self):
       for employee in self._employees:
           if employee.role == "Developer":
               print(f"{employee.name} - {employee.role}")

def main():
   it_department = ITDepartment()
   it_department.add_employee(Employee("John Doe", "Developer"))
   it_department.add_employee(Employee("Jane Doe", "Manager"))
   it_department.list_employees()

if __name__ == '__main__':
   main()


