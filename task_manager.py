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

    print("LOGIN\n")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("\033[41m User does not exist \033[0m")
        continue
    elif username_password[curr_user] != curr_pass:
        print("\033[41m Wrong password \033[0m")
        continue
    else:
        print("\033[42m Login Successful! \033[0m")
        logged_in = True


# This function is called when the user selects 'r' and it allows a user to be registered.
def reg_user():
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            # If the username already exists, an error message is printed and user can try again.
            print("\033[41m Sorry, this username already exists. \033[0m")
            continue
        else:
            break   
    
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("\033[42m New user added \033[0m")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise it presents an error message.
    else:
        print("\033[41m Passwords do no match \033[0m")


# This function  is called when a user selects 'a' and it allows a user to add a new task.      
def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''
    
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username in username_password.keys():
            break
        else:
            # If the user does not exist, an error message is printed.
            print("\033[41m User does not exist. Please enter a valid username \033[0m")

            
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    
    while True:    
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            # If the date is not in the specified format, an error message is printed.
            print("\033[41m Invalid datetime format. Please use the format specified \033[0m")
    
    #  Then get the current date.
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
    print("\033[42m Task successfully added.\033[0m")


# This function is called when users type 'va' and it allows the user to view all tasks listed in tasks.txt.
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)'''

    for t in task_list:
        print("_______________________________")
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print("_______________________________")


# This function is called when users type 'vm' and it allows the user to view all the tasks assigned to them.                   
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)    '''
    
    task_num = 0
    task_num_list = []
    tasks_assigned = False

    for t in task_list:
        task_num += 1        
        if t['username'] == curr_user:
            task_num_list.append(task_num)
            tasks_assigned = True
            print("_______________________________")
            disp_str = f"Task number: \t\t {task_num}\n"
            disp_str += f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Task Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)
            print("_______________________________")
        if not tasks_assigned:
              # If user has no tasks assigned then error message is printed.  
            print("\033[41m You currently have no tasks assigned to you. \033[0m")


    # This function is called when a user chooses to change who the task is assigned to.
    def update_task_assignment(task_index, change_username):
        task_list[task_index]['username'] = change_username
        print("_______________________________")
        print(f"\033[42m You have assigned task number {select_task} to {change_username}. \033[0m")
        print("_______________________________")

        # Update tasks.txt to reflect the changed assignment
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


    # This function is called to allow the user to mark tasks as completed.            
    def mark_task_complete(task_index):
        task_list[task_index]['completed'] = True
        print("_______________________________")
        print(f"\033[42m Task Number {select_task} has been marked as complete.\033[0m")
        print("_______________________________")

        # Update tasks.txt to reflect the changed completed status
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


    # This function is called to change the due date of a task.            
    def change_due_date(task_index, change_date_string):
        change_date = datetime.strptime(change_date_string, DATETIME_STRING_FORMAT)
        task_list[task_index]['due_date'] = change_date
        print("_______________________________")
        print(f"\033[42m You have updated the due date of task number {select_task}.\033[0m")
        print("_______________________________")

        # Update tasks.txt to reflect the new due date for that task
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


    # The user is given an option to edit the task or return to main menu.
    while True:
        select_task = input("""
Please select a task to edit by entering the task number.
Enter '-1' to return to the main menu: 
_______________________________ """)
    
        if select_task == "-1": 
            # If user enters -1, they return to the main menu.
            print(menu)
            break        
        elif not select_task.isnumeric():
            # If the user does not enter a number then an error message is printed.
            print("\033[41m Sorry, this is not a valid number.\033[0m")
            continue            
        
        elif int(select_task) in task_num_list:
            # If the user selects a task that is assigned to them they can mark it as complete or edit it or return to main menu.
            edit_task = input("Would you like to:\n 1. Mark task as complete\n 2. Edit the task\n 3. Back to main menu\n")
            task_index = int(select_task) -1

            if edit_task == "1":
                # The selected task is marked complete.
                mark_task_complete(task_index)

            elif edit_task == "2":
                # The user can choose whether they want to assign the selected task to a different user, or change the task due date.
                task_edit = input("Would you like to:\n 1. Assign the task to a different user\n 2. Change the due date of the task:\n")
                if task_edit == "1":  
                    if not task_list[task_index]['completed']:                  
                        change_username = input("Who would you like to assign the task to? ")                    
                        if change_username in username_password.keys():
                            update_task_assignment(task_index, change_username)
                        else:
                            # If the username does not exist, an error message is printed.
                            print("\033[41m\n Sorry, user does not exist.\033[0m\n Please enter a valid username: ")
                    else:
                        # If the task is already marked as complete, an error message is printed.
                        print("\033[41m\n Task is already completed and cannot be re-assigned.\033[0m")


                elif task_edit == "2":
                    if not task_list[task_index]['completed']:
                        # If selected task is not completed, they can edit the due date.
                        try:
                            change_date = input("Please enter new due date (YYYY-MM-DD) : ")
                            change_due_date(task_index, change_date)
                            break
                        except ValueError:
                            # If due date is not in the specified format, an error message is printed.
                            print("\033[41m Invalid datetime format. Please use the format specified.\033[0m")
                    else:
                        print("\033[41m\n Task is already completed and the due date cannot be changed.\033[0m")
                
                else:
                    # If the user enters a number that is not listed, an error message is printed.
                    print("\033[41m Sorry, that is not an option.\033[0m")

            elif edit_task == "3":
                # The user returns to main menu.
                break
        else:
            # If the user input is not recognised, an error message is printed.
            print("\033[41m\nSorry, this is incorrect.\033[0m")
        

# This function is called to create two text files and print out overview information on tasks and users.            
def generate_reports():
    print("\033[42m Your report has been generated. You can open it in a separate window.\033[0m")
    # Task overview variables
    number_of_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    curr_date = datetime.today()
    overdue_tasks = 0
    overdue_incomplete_tasks = 0

    for t in task_list:
        # Calculates the total number of tasks by adding one each time there is a tast in task list.
        number_of_tasks += 1

        # If task marked as complete in task list then adds 1 and calculates total number of completed tasks.
        if t['completed'] == True:
            completed_tasks += 1
        else:
            # If task not marked complete then adds 1 and calculated total number of uncompleted tasks.
            uncompleted_tasks += 1

        # If current date is later than the due date then task counts as overdue and calculates the total number of overdue and uncompleted tasks.
        if curr_date > t['due_date']:
            overdue_tasks += 1

        # If current date is later than the due date and tasks is not completed, counts task and overdue and uncomplete.
        if curr_date > t['due_date'] and t['completed'] == "No":
            overdue_incomplete_tasks_per_user += 1

        if number_of_tasks != 0:
            # If the user has tasks assigned to them, this calculates the percentage of tasks they have completed 
            percent_incomplete = (uncompleted_tasks / number_of_tasks) * 100
            percent_incomplete = round(percent_incomplete, 2)
            # And the percentage of overdue tasks.
            percent_overdue = (overdue_tasks / number_of_tasks) * 100
            percent_overdue = round(percent_overdue, 2)
        else:
            percent_incomplete = 0
            percent_overdue = 0
        
   
    # Creates new file called task overview for the user to view
    with open ("task_overview.txt", "w+") as task_overview:
        task_overview.write(f"The total number of tasks in Task Manager is:\t {number_of_tasks}\n______________________________________________________________\n")
        task_overview.write(f"The total number of completed tasks is:\t {completed_tasks}\n______________________________________________________________\n") 
        task_overview.write(f"The total number of uncompleted tasks is:\t {uncompleted_tasks}\n______________________________________________________________\n")
        task_overview.write(f"The total number of uncompleted and overdue tasks is:\t {overdue_incomplete_tasks}\n______________________________________________________________\n")
        task_overview.write(f"The percentage of tasks that are incomplete:\t {percent_incomplete}%\n______________________________________________________________\n")
        task_overview.write(f"The percentage of tasks that are overdue is:\t {percent_overdue}%\n______________________________________________________________\n")

    # User overview variables
    number_of_users = 0
    tasks_per_user = 0
    completed_tasks_user = 0
    uncompleted_tasks_user = 0
    curr_date = datetime.today()
    overdue_tasks_per_user = 0
    overdue_incomplete_tasks_per_user = 0
    

    # Calculates the total number of users by adding one each time there is a user in user data
    for user in user_data:
        number_of_users += 1 

    # Calculates the total number of tasks assigned to current user by counting the tasks in task list that have the same username as current user
    for t in task_list:
        if t['username'] == curr_user:
            tasks_per_user += 1          

        # Calculates the percentage of tasks that the current user has completed -> (completed tasks user / number of tasks) * 100
            if t['completed']:
                completed_tasks_user += 1
            else:
                uncompleted_tasks_user += 1
    
            # If current date is later than the due date then task counts as overdue and calculates the total number of overdue tasks per user.
            if curr_date > t['due_date']:
                overdue_tasks_per_user += 1

            # If current date is later than the due date and tasks is not completed, counts task and overdue and uncomplete.
            if curr_date > t['due_date'] and t['completed'] == "No":
                overdue_incomplete_tasks_per_user +1
        
        # Calculates the percentage of tasks assigned to current user and tasks completed, uncompleted, overdue by current user.
        if tasks_per_user != 0:
            percent_per_user = (tasks_per_user / number_of_tasks) * 100 
            percent_complete_per_user = (completed_tasks_user / tasks_per_user) * 100
            percent_uncompleted_per_user = (uncompleted_tasks_user / tasks_per_user) * 100
            percent_uncompleted_overdue_per_user = (overdue_incomplete_tasks_per_user / tasks_per_user) * 100
        else:
            percent_per_user = 0
            percent_complete_per_user = 0
            percent_uncompleted_per_user = 0
            percent_uncompleted_overdue_per_user = 0
    

    # Creates new file called user overview for the user to view
    with open("user_overview.txt", "w+") as user_overview:
        user_overview.write(f"The total number of registered users is:\t {number_of_users}\n______________________________________________________________\n")
        user_overview.write(f"The total number of tasks in Task Manager is:\t {number_of_tasks}\n______________________________________________________________\n")
        user_overview.write(f"The total number of tasks assigned to you are:\t {tasks_per_user}\n______________________________________________________________\n")
        user_overview.write(f"The percentage of total number of tasks that have been assigned to you is:\t {percent_per_user}% \n______________________________________________________________\n")
        user_overview.write(f"The percentage of your tasks that have been completed is:\t {percent_complete_per_user}%\n______________________________________________________________\n")
        user_overview.write(f"The percentage of your tasks that have not been completed is:\t {percent_uncompleted_per_user}% \n______________________________________________________________\n")
        user_overview.write(f"The percentage of your tasks that are overdue and uncompleted is:\t {percent_uncompleted_overdue_per_user}% \n______________________________________________________________\n")


# This function is called to allow the admin to display statistics so that the reports generated are read from tasks.txt and user.txt and displayed on the screen.
def user_statistics():
    curr_date = datetime.today()

    # A dictionary to store the completed, uncompleted, and overdue tasks for each user in user.txt.
        
    user_reports = {}

    for t in task_list:
        username = t['username']


        if username not in user_reports:
            # If username is not in the dictionary, automatically populate zero completed and uncompleted tasks.
            user_reports[username] = {'completed_tasks': 0, 'uncompleted_tasks': 0, 'overdue_tasks': 0}

        
        if t['completed']:
            user_reports[username]['completed_tasks'] += 1
        else:
            user_reports[username]['uncompleted_tasks'] += 1

        # If current date is later than the due date then task counts as overdue.
        if curr_date > t['due_date']:
            user_reports[username]['overdue_tasks'] += 1

    for user, report in user_reports.items():
        # Calculate total number of tasks per user in user report.
        total_tasks = report['completed_tasks'] + report['uncompleted_tasks']
        if total_tasks != 0:
            # If the user has tasks assigned to them, this calculates the percentage of tasks they have completed.
            percent_complete = (report['completed_tasks'] / total_tasks) * 100
            percent_overdue = (report['overdue_tasks'] / total_tasks) * 100

        else:
            percent_complete = 0

        # Display the statistics to admin
        print("______________________________________________________________")
        print(f"User: {user}")
        print(f"Total tasks for user: {total_tasks}")
        print(f"Completed tasks: {report['completed_tasks']} ")
        print(f"Tasks to be completed: {report['uncompleted_tasks']} ")
        print(f"Percentage of tasks completed: {percent_complete}%")
        print(f"Percentage of overdue tasks: {percent_overdue}%")
        print("______________________________________________________________")

#====Menu Section====
# A menu is presented to the user so that they can choose which action they would like.

while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics (admin only)
e - Exit
: ''').lower()

    if menu == "r":
        reg_user()

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine()

    elif menu == "gr":
        generate_reports()
           
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        user_statistics()

        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

        # Displays user statistics to admin.
          

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("\033[41m You have made a wrong choice. Please Try again \033[0m")