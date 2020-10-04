from datetime import datetime


"""calc_days_worked

Keyword arguments: date_1, date_2
argument -- Calculate how many days the employee has worked on a project
Return: returns the number of days an employee has worked on a project. 
If second date is indicated as NULL, then that date is read as the current date 

"""


def calc_days_worked(date_1, date_2):
    if date_2 == "NULL":
        d1 = datetime.strptime(date_1, "%Y-%m-%d")
        d2 = datetime.today()
    else:
        d1 = datetime.strptime(date_1, "%Y-%m-%d")
        d2 = datetime.strptime(date_2, "%Y-%m-%d")

    return str(abs((d2-d1).days))


"""sort_line

Keyword arguments: raw_data
argument -- Sorts the raw list of dictionaries into an ordered list of dictionaries,
which are centered around the projects 
Return: returns a list of dictionaries 

"""


def sort_data(raw_data):
    orderded_data = list()
    for i in raw_data:
        days_worked = calc_days_worked(i["DateFrom"], i["DateTo"])

        # If these is no project with the same ID initiated in the list, initiate it
        if next((item for item in orderded_data if item["ProjectID"] == i["ProjectID"]), None) is None:
            orderded_data.append({
                "ProjectID": i["ProjectID"], "EmpID": i["EmpID"], "DaysWorked": days_worked})
        # If there is a project with that number initiated in the list, add the new employees
        # and how much they have worked
        else:
            for items in orderded_data:
                if items["ProjectID"] == i["ProjectID"]:
                    items["EmpID"] += " " + i["EmpID"]
                    items["DaysWorked"] += " " + days_worked

    # Fix nested lists
    for item in orderded_data:
        item["DaysWorked"] = item["DaysWorked"].split()
        item["EmpID"] = item["EmpID"].split()

    return find_winners(orderded_data)


"""find_winners

Keyword arguments: sorted_data 
argument -- Finds the two biggest numbers and their corresponding employees
Return: a print statement of which pair did the most in every project

"""


def find_winners(sorted_data):
    for i in sorted_data:
        biggest_number = 0
        second_biggest = 0
        index_first = None
        index_second = None

        # Find the two biggest numbers in the Days worked list get
        # the corresponding indexes for the employees
        for x in i["DaysWorked"]:
            if int(x) > biggest_number:
                biggest_number = int(x)
            elif int(x) > second_biggest and int(x) < biggest_number:
                second_biggest = int(x)

        index_first = i["DaysWorked"].index(str(biggest_number))
        index_second = i["DaysWorked"].index(str(second_biggest))
        print(
            f'The pair which worked on project {i["ProjectID"]} the most hours are employees {i["EmpID"][index_first]} and {i["EmpID"][index_second]}, who worked {biggest_number} and {second_biggest} days, respectively!')


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

            sort_data(raw_data)

    # If there is no file present catch the exceptipon
    except FileNotFoundError as error:
        print(error)


if __name__ == "__main__":
    sort_employees("employee_projects.txt")
