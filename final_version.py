from datetime import datetime
from collections import namedtuple


class Employee:
    def __init__(self, empID, projID, dateFrom, dateTo):
        self.empID = empID
        self.projID = projID
        self.dateFrom = dateFrom
        self.dateTo = dateTo

    # Convert the date in a datetime variable
    def DateConversion(self, otherDateFrom, otherDateTo):
        if (self.dateTo == "NULL") and (otherDateTo == "NULL"):
            date_1 = datetime.strptime(self.dateFrom, "%Y-%m-%d")
            date_2 = datetime.today()
            other_date_1 = datetime.strptime(otherDateFrom, "%Y-%m-%d")
            other_date_2 = datetime.today()
        elif otherDateTo == "NULL":
            other_date_1 = datetime.strptime(otherDateFrom, "%Y-%m-%d")
            other_date_2 = datetime.today()
            date_1 = datetime.strptime(self.dateFrom, "%Y-%m-%d")
            date_2 = datetime.strptime(self.dateTo, "%Y-%m-%d")
        elif self.dateTo == "NULL":
            date_1 = datetime.strptime(self.dateFrom, "%Y-%m-%d")
            date_2 = datetime.today()
            other_date_1 = datetime.strptime(otherDateFrom, "%Y-%m-%d")
            other_date_2 = datetime.strptime(otherDateTo, "%Y-%m-%d")
        else:
            date_1 = datetime.strptime(self.dateFrom, "%Y-%m-%d")
            date_2 = datetime.strptime(self.dateTo, "%Y-%m-%d")
            other_date_1 = datetime.strptime(otherDateFrom, "%Y-%m-%d")
            other_date_2 = datetime.strptime(otherDateTo, "%Y-%m-%d")

        return [date_1, date_2, other_date_1, other_date_2]

    # Calculates the intersect of days from the two date ranges
    def TimeWorkedTogether(self, otherDateFrom, otherDateTo):
        dateInfo = self.DateConversion(otherDateFrom, otherDateTo)
        Range = namedtuple('Range', ['start', 'end'])

        range_1 = Range(start=dateInfo[0], end=dateInfo[1])
        range_2 = Range(start=dateInfo[2], end=dateInfo[3])
        latest_start = max(range_1.start, range_2.start)
        earliest_end = min(range_1.end, range_2.end)
        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)

        return overlap


"""find_winner

Keyword arguments: employee_file
argument -- Opens the txt file and populates the data into a list of dictionaries.
That data is then processed and a winner couple is deduced
Return: None

"""


def find_winner(employee_file):
    try:
        file_employees = open(employee_file, "r")
        IDs = list()
        raw_data = list()
        time_work_together = 0
        best_couple = list()

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

            # Search through the employee class objects to see who worked on the same projects
            for i in employees:
                for d in employees:
                    # This will show couples mirrored as well, which is not an issue because bellow they are stored and checked in a list
                    if (employees[i].projID == employees[d].projID) and (employees[i].empID != employees[d].empID):
                        # Update the days worked
                        time_work_together = employees[i].TimeWorkedTogether(
                            employees[d].dateFrom, employees[d].dateTo)
                        # If couple is not in the list, then add it
                        if next((item for item in best_couple if item["EmpID"] == [employees[i].empID, employees[d].empID]), None) is None:
                            keys = ["EmpID", "ProjectID", "WorkingTime"]
                            values = [[employees[i].empID, employees[d].empID],
                                      employees[d].projID, time_work_together]
                            best_couple.append(dict(zip(keys, values)))
                        # If its in the list, check which couple it is and add the days to it and relevant project
                        else:
                            for emps in best_couple:
                                if emps["EmpID"] == [employees[i].empID, employees[d].empID]:
                                    emps["ProjectID"] += " " + \
                                        employees[d].projID
                                    emps["WorkingTime"] += time_work_together

            # Find the most days worked by a couple on a mutual project and which one
            most_hours_worked = max([x["WorkingTime"] for x in best_couple])
            winner_index = next((index for (index, d) in enumerate(
                best_couple) if d["WorkingTime"] == most_hours_worked), None)

            print(
                f'Employees {best_couple[winner_index]["EmpID"][0]} and {best_couple[winner_index]["EmpID"][1]} worked together on project/s {best_couple[winner_index]["ProjectID"]} for {best_couple[winner_index]["WorkingTime"]} days in total')
            print("This is the longest a couple has worked on mutual projects!")

            # If there is no file present catch the exceptipon
    except FileNotFoundError as error:
        print(error)


if __name__ == "__main__":
    find_winner("employee_projects.txt")
