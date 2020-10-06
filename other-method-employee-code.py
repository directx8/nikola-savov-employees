from datetime import datetime


class Employee:
    def __init__(self, empID, projID, dateFrom, dateTo):
        self.empID = empID
        self.projID = projID
        self.dateFrom = dateFrom
        self.dateTo = dateTo

    def employeeID(self):
        pass

    def projectID(self):
        pass

    def timeWorked(self):
        if self.dateTo == "NULL":
            d1 = datetime.strptime(self.dateFrom, "%Y-%m-%d")
            d2 = datetime.today()
        else:
            d1 = datetime.strptime(self.dateFrom, "%Y-%m-%d")
            d2 = datetime.strptime(self.dateTo, "%Y-%m-%d")

        return str(abs((d2-d1).days))


"""sort_employees

Keyword arguments: employee_file 
argument -- Opens the txt file and populates the data into a list of dictionaries
Return: None

"""


def sort_employees(employee_file):
    try:
        file_employees = open(employee_file, "r")
        IDs = list()
        raw_data = list()

        # If file is accecible then you can continue with the rest of the code
        if file_employees.readable():
            count = 0

            # Populate a list with dictionaries from each line
            for line in file_employees:
                if count == 0:
                    IDs = ((line.rstrip()).split(', '))
                    count = None
                else:
                    tmp = ((line.rstrip()).split(', '))
                    raw_data.append(dict(zip(IDs, tmp)))

            # Create object dictionary for the employees
            employees = {i: Employee(
                d["EmpID"], d["ProjectID"], d["DateFrom"], d["DateTo"]) for i, d in enumerate(raw_data)}

            time_work_together = 0
            for i in employees:
                for d in employees:
                    if (employees[i].projID == employees[d].projID) and (employees[i].empID != employees[d].empID):
                        if time_work_together < (int(employees[i].timeWorked()) + int(employees[d].timeWorked())):
                            time_work_together = int(employees[i].timeWorked(
                            )) + int(employees[d].timeWorked())
                            print(
                                f'Employees {employees[i].empID} and {employees[d].empID} worked together on project {employees[d].projID} for {time_work_together} days')

                       # If there is no file present catch the exceptipon
    except FileNotFoundError as error:
        print(error)


if __name__ == "__main__":
    sort_employees("employee_projects.txt")
