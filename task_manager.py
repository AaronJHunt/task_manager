# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# REGISTER USER
def reg_user():
    '''Add a new user to the user.txt file'''

    # assume new username is taken until checked against stored usernames
    user_taken = True
    while user_taken == True:
        # - Request input of a new username
        new_username = input("New Username: ")

        # check new username agains stored usernames, if it exists get user to try a different name
        if new_username in username_password:
            print("Username already exists, try a different one.")
        elif new_username not in username_password[username]:
            user_taken = False

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

# ADD TASK
# add a new task for a user
def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        break

# VIEW ALL
# view all tasks regardless of user
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
    # for all tasks we print out all the information in a readable way.
    # we also include index in the for loop which we start at 1, this is to number the tasks
    for index, t in enumerate(task_list, start=1):
        disp_str = f"Task no. {index}--------------------\n"
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += "Task Complete:  \t{}\n".format("Yes" if t['completed'] else "No")
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# VIEW MINE
# view all tasks associated with logged in user
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    
    # for all tasks that are assigned to current user we print out all the information in a readable way.
    # we also include index in the for loop which we start at 1, this is to number the tasks
    for index, t in enumerate(task_list, start=1): 
        if t['username'] == curr_user:
            disp_str = f"Task no. {index}--------------------\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += "Task Complete: \t {}\n".format("Yes" if t['completed'] else "No")
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    # allow user to select a task based on the number to manipulate the data
    while True:
        task_select = int(input("Select a specific task or go back to menu(-1): "))
        
        # check that user hasnt selected to go to menu and that the number is less than or equal to the number of tasks
        # also make sure task is assigned to the user
        if (task_select  != -1) and (task_select <= len(task_list)) and (task_list[task_select-1]['username'] == curr_user):
            task_option = input('''Select an option:
    c - mark as complete
    e - edit the task 
    : ''').lower()

            if task_option == 'c':
                mark_task_complete(task_select)

            elif task_option == 'e':
                edit_task(task_select)

            else:
                print("Back to menu")
            break
        elif (task_select  != -1) and (task_select <= len(task_list)) and (task_list[task_select-1]['username'] != curr_user):
            print("This is not your task, please select another one.")
            continue
        elif task_select == -1:
            break
        else:
            print("Not a valid task number, please try again.")
            continue

# MARK TASK AS COMPLETE
# marks task as complete using parameters passed
def mark_task_complete(task):

    # check if selected task is already set to completed, if not set to completed and update the task file
    if (task_list[task-1]['completed'] == False):
        task_list[task-1]['completed'] = True
        print(f"Task {task} marked as completed.")
        update_task_file()

    else:
        print("Task is already marked as completed.")
    
            
# EDIT TASK
# edit task using parameters passed
def edit_task(task):
    # check if selected task is set to complete, if not then allow user to edit
    if (task_list[task-1]['completed'] == False):

        # check username exists before assigning it to the task
        while True:
            updated_user = input("Updated username: ")
            if updated_user not in username_password.keys():
                print("Username doesn't exist, try again.")
                continue
            updated_due_date = input("Updated due date (YYYY-MM-DD): ")
            for index, t in enumerate(task_list, start=1):
                if (t['username'] == curr_user) and (index == task):
                    # update task
                    t['username'] = updated_user
                    t['due_date'] = datetime.strptime(updated_due_date, DATETIME_STRING_FORMAT)
            print(f"Task {task} has been edited.")
            update_task_file()
            break
    else:
        print("Task cant be edited as it is already completed")

# UPDATE TASK FILE
# rewrites data to the tasks.txt file
def update_task_file():
    with open("tasks.txt", "w") as task_file:

        # for all the tasks in task list, build up a list called str_attrs and append to task_list_to_write list seperated by semicolons
        # then write to tasks.txt file joining all entries in task_list_to_write with a newline.
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task file updated.")

# GENERATE REPORTS
# generates 2 reports for task overview and user overview
def generate_reports():
    print("Generating reports...")

    # setup variables to hold task data
    tasks_generated = len(task_list)
    tasks_completed = 0
    tasks_uncompleted = 0
    tasks_overdue = 0
    
    # loop through each task and update corresponding variables
    for task in task_list:
        if task['completed'] == True:
            tasks_completed += 1
        else:
            tasks_uncompleted +=1

        if (task['due_date'].date() < date.today()) and task['completed'] == False:
            tasks_overdue += 1
        else:
            tasks_overdue += 0

    # variable to hold percentages values, rounded to 2 decimal places
    tasks_percentage_incomplete = round((tasks_uncompleted / tasks_generated) * 100,2)
    tasks_percentage_overdue = round((tasks_overdue / tasks_generated) * 100,2)

    # Building the string to save to task_overview.txt
    task_overview_str = "-------------------------------\n"
    task_overview_str += "Tasks Overview Report\n"
    task_overview_str += "-------------------------------\n"
    task_overview_str += f"Generated:\t\t\t\t {tasks_generated}\n"
    task_overview_str += f"Completed:\t\t\t\t {tasks_completed}\n"
    task_overview_str += f"Uncompleted:\t\t\t {tasks_uncompleted}\n"
    task_overview_str += f"Overdue: \t\t\t\t {tasks_overdue}\n"
    task_overview_str += f"Percentage incomplete: \t {tasks_percentage_incomplete}%\n"
    task_overview_str += f"Percentage Overdue: \t {tasks_percentage_overdue}%"
    #print(task_overview_str)

    with open('task_overview.txt', 'w') as f:
        f.write(task_overview_str)

    # USER OVERVIEW REPORT
    # generate and build user overview report and save to user_overview.txt
    user_number = len(username_password.keys())
    tasks_generated = len(task_list)

    # Building user overview string
    user_overview_str = "-------------------------------\n"
    user_overview_str += "User Overview Report\n"
    user_overview_str += "-------------------------------\n"
    user_overview_str += f"Number of users: \t\t{user_number}\n"
    user_overview_str += f"Total tasks generated: \t{tasks_generated}\n"
    user_overview_str += "User Tasks breakdown :- \n"

    # loop through all users
    for user in username_password:
        # variable to hold each users data
        user_tasks = 0
        user_tasks_completed = 0
        user_tasks_incomplete = 0
        user_tasks_overdue = 0
        
        # loop through tasks and populate user variables
        for t in task_list:
            if t['username'] == user:
                user_tasks +=1
                if t['completed']:
                    user_tasks_completed += 1
                else:
                    user_tasks_incomplete += 1

                if (t['due_date'].date() < date.today()) and t['completed'] == False:
                    user_tasks_overdue += 1
                else:
                    user_tasks_overdue += 0

        # user variables to hold calculated percentages
        user_tasks_p = round((user_tasks / len(task_list)) * 100,2)

        # error handling to stop zero division errors when the user has no tasks assigned
        try:
            user_tasks_completed_p = round((user_tasks_completed / user_tasks) * 100, 2)
        except ZeroDivisionError:
            user_tasks_completed_p = 0
        
        try:
            user_tasks_incomplete_p = round((user_tasks_incomplete / user_tasks) * 100, 2)
        except ZeroDivisionError:
            user_tasks_incomplete_p = 0

        try:
            user_tasks_overdue_p = round((user_tasks_overdue / user_tasks) * 100, 2)
        except ZeroDivisionError:
            user_tasks_overdue_p = 0

        # user specific additions to the user overview string
        user_overview_str += f"\tUsername: \t\t\t{user}\n"
        user_overview_str += f"\tAssigned tasks: \t\t{user_tasks}\n"
        user_overview_str += f"\tPercentage assigned(%): {user_tasks_p}%\n"
        user_overview_str += f"\tCompleted user tasks: \t{user_tasks_completed_p}%\n"
        user_overview_str += f"\tIncomplete user tasks: \t{user_tasks_incomplete_p}%\n"
        user_overview_str += f"\tOverdue user tasks: \t{user_tasks_overdue_p}%\n"
        user_overview_str += "\n"
    
    # save string to user_overview.txt
    with open('user_overview.txt', 'w') as f:
        f.write(user_overview_str)

# DISPLAY STATISTICS
# Displays the statistic of number of tasks and users
def display_stats():
    '''If the user is an admin they can display statistics about number of users
    and tasks.'''
    # setup variables to hold statistics
    num_users = 0
    num_tasks = 0

    # try open tasks.txt file, if it exists then set num_taks to lines in file
    # if it doesnt exist we create a blank file
    try:
        with open('tasks.txt', 'r') as tasks:
            num_tasks = len(tasks.readlines())
    except FileNotFoundError:
        with open('tasks.txt', 'w') as tasks:
            tasks.write()

    # try open user.txt file, if it exists then set num_users to lines in file
    # if it doesnt we create the file with admin set up
    try:
        with open('user.txt', 'r') as users:
            num_users = len(users.readlines())
    except FileNotFoundError:
        with open('user.txt', 'w') as users:
            users.write("admin;password")

    # print out the statistics in a readable way
    print("-----------------------------------")
    print("Statistics")
    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")  

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()

    # based on user selection call the relative function
    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
                
    elif menu == 'gr':
        generate_reports()
    
    elif menu == 'ds' and curr_user == 'admin': 
        display_stats()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
