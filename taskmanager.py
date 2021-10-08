# This python program helps to manage tasks assigned to each member of the team
# for a small business.

from datetime import date
count = 0
task_choice = ""
line = ""
user_file = ""
user_found = False
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
          'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
total_tasks = 0


# The reg_user function is called when the user selects 'r' to register a user
def reg_user():
    # Create a boolean variable
    user_exists = False
    new_user = input("Enter username you wish to register:\n")
    with open('user.txt', 'r', encoding='utf-8') as reg_file:
        for reg_line in reg_file:
            if reg_line.split(', ')[0] == new_user:
                user_exists = True

    # Keep asking for a valid username if it clashes
    while user_exists:
        print("Error, Username already exists, PLease input a new one")
        new_user = input("Enter username you wish to register:\n")
        with open('user.txt', 'r', encoding='utf-8') as reg_file:
            for reg_line in reg_file:
                if reg_line.split(', ')[0] == new_user:
                    user_exists = True
                    break
                else:
                    user_exists = False

    # If username is unique, proceed to ask for a password
    if not user_exists:
        new_password = input("Enter password you wish to register:\n")
        confirm_password = input("Please confirm password:\n")

        # Check if passwords match
        while confirm_password != new_password:
            print("Passwords do not match, please try again. Please confirm password")
            confirm_password = input("Please confirm password:\n")

        if new_password == confirm_password:
            reg_file = open('user.txt', 'a', encoding='utf-8')
            reg_file.write('\n' + new_user + ', ' + new_password)
            reg_file.close()
            print(f"You have registered {new_user} as a user.")


# The add_task function is called when the user selects 'a' to add a new task
def add_task():
    # Learnt how to use the 'date' class, module and object here
    # https://www.programiz.com/python-programming/datetime/current-datetime
    from datetime import date
    name = input('Enter the name of person task is assigned to:\n')
    title = input("Enter the title of the task:\n")
    description = input("Enter the description of the task:\n")
    due_date = input("Enter the due date of the task: \n")
    today_date = date.today()
    # Convert date object to a string
    t_date = today_date.strftime("%d %b %Y")
    completed = 'No'
    # append task data to a list, convert the list to a string and save to the tasks.txt file
    tasks = [name, title, description, t_date, due_date, completed]
    with open('tasks.txt', 'a', encoding='utf-8') as add_task_file:
        add_task_file.writelines('\n' + ", ".join(tasks))


# The view_all function is called when the user selects 'va' to view all  the tasks in 'tasks.txt'
# It accepts a list as an argument
def view_all(output_list):
    with open('tasks.txt', 'r', encoding='utf-8') as va_task_file:
        for va_line in va_task_file:
            print("----------------------------------------------------------------------------------------")
            for cat in output_list:
                # Get the index of the output in the list and match it with the data in the task file
                # Learnt how to use the index method here: https://www.w3schools.com/python/ref_list_index.asp
                index = output_list.index(cat)
                data = va_line.split(', ')[index]

                # Learnt how to use the "just" method here:
                # https://www.programiz.com/python-programming/methods/string/ljust
                # The "just" method returns the left-justified string within the given minimum width
                print(f"{cat.ljust(30)} {data}")


# The view_mine function is called when the user selects 'vm' to view all the that's been assigned to them
# It accepts the user's username as argument
def view_mine(username):
    # Create a boolean variable
    global user_found
    user_found = False
    # Initialise a counter
    global count
    count = 0
    with open('tasks.txt', 'r', encoding='utf-8') as vm_task_file:
        for vm_line in vm_task_file:
            # if the user has been assigned tasks, display such tasks
            if username in vm_line.split(', '):
                user_found = True
                output = ['Assigned to:', 'Task:', 'Task Description:', 'Date assigned:', 'Due date:',
                          'Task complete?']
                # Count the number of tasks
                count += 1
                print(count)
                print("-------------------------------------------------------------------------------------")
                for cat in output:
                    index = output.index(cat)
                    data = vm_line.split(', ')[index]

                    print(f"{cat.ljust(30)} {data}")

        # Display a message if the user has not been assigned any tasks
        if not user_found:
            print("\nOOps, you have not been assigned any tasks.")

            print()
            main_menu()


# The mark_task_complete function is called when the user wants to mark their task as complete
def mark_task_complete():
    # Initialise a counter
    occur = 0
    with open('tasks.txt', 'r', encoding='utf-8') as m_task_file:
        # Read all the file content into memory
        lines_list = m_task_file.readlines()

        for tasks in lines_list:
            if tasks.strip('\n').split(', ')[0] == user:
                occur += 1
                # if the counter equals the task choice, remove and return the task list
                if occur == task_choice:
                    index = lines_list.index(tasks)
                    task = lines_list.pop(index)
                    break

        # change the 'No' to 'Yes'
        task = task.strip('\n').split(', ')
        task[5] = 'Yes\n'
        # add the task back to the task list
        lines_list.insert(index, ', '.join(task))

    # write the new task list into the file
    with open('tasks.txt', 'w', encoding='utf-8') as m_task_file:
        m_task_file.writelines(lines_list)


# The edit_task_reassign function is called when the user wants to reassign their tasks to someone else
# It accepts the user's username as argument
def edit_task_reassign(new_user):
    with open('tasks.txt', 'r', encoding='utf-8') as e_task_file:
        # Read all the file content into memory
        occur = 0
        lines_list = e_task_file.readlines()

        for tasks in lines_list:
            if tasks.strip('\n').split(',')[0] == user:
                occur += 1
                # if the counter equals the task choice, remove and return the task list
                if occur == task_choice:
                    task = lines_list.pop(lines_list.index(tasks))
                    break

        # reassign
        task = task.strip('\n').split(', ')
        task[0] = new_user
        # add the task back to the task list
        lines_list.append(', '.join(task))

        # write the new task list into the file
    with open('tasks.txt', 'w', encoding='utf-8') as e_task_file:
        e_task_file.writelines(lines_list)


# The edit_task_date function is called when the user wants to edit the due date of their task
# It accepts the new date as argument
def edit_task_date(new_date):
    with open('tasks.txt', 'r', encoding='utf-8') as e_task_file:
        # Read all the file content into memory
        occur = 0
        lines_list = e_task_file.readlines()

        for tasks in lines_list:
            if tasks.strip('\n').split(',')[0] == user:
                occur += 1
                # if the counter equals the task choice, remove and return the task list
                if occur == task_choice:
                    task = lines_list.pop(lines_list.index(tasks))
                    break

        # change the due date
        task = task.strip('\n').split(', ')
        task[4] = new_date
        # add the task back to the task list
        lines_list.append(', '.join(task))

        # write the new task list into the file
    with open('tasks.txt', 'w', encoding='utf-8') as e_task_file:
        e_task_file.writelines(lines_list)


# The can_be_edited function returns a True or False if the task can be edited or not
# based on if it has been completed or not
def can_be_edited():
    with open('tasks.txt', 'r', encoding='utf-8') as e_task_file:
        # Read all the file content into memory
        occur = 0
        lines_list = e_task_file.readlines()

        for tasks in lines_list:
            if tasks.strip('\n').split(',')[0] == user:
                occur += 1
                # if the counter equals the task choice, remove and return the task list
                if occur == task_choice:
                    task = lines_list.pop(lines_list.index(tasks))
                    if task.strip('\n').split(', ')[5] == "No":
                        return True
                    else:
                        return False


# The task_overview function generates a 'task_overview.txt' file that stores the statistics of the task
def task_overview():
    global total_tasks
    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue = 0

    with open('tasks.txt', 'r', encoding='utf-8') as task_stat:
        global months
        import datetime

        for tasks in task_stat:
            # Get the due date string
            due_date = tasks.strip('\n').split(', ')[4]
            # split into day, month and year
            day, month, year = due_date.split(" ")[0], due_date.split(" ")[1], due_date.split(" ")[2]
            # set the month in words to a matching month number in the dict
            for mon in months.keys():
                if mon == month:
                    month = months[mon]
                    break
            # Convert the date string to a date object
            overdue_date = datetime.date(int(year), int(month), int(day))

            if tasks.strip('\n').split(', ')[5] == 'Yes':
                completed_tasks += 1
            elif (tasks.strip('\n').split(', ')[5] == 'No') and (date.today() >= overdue_date):
                overdue += 1
            elif tasks.strip('\n').split(', ')[5] == 'No':
                uncompleted_tasks += 1

            total_tasks += 1

    uncompleted_percent = round((uncompleted_tasks / total_tasks) * 100, 2)
    overdue_percent = round((overdue / total_tasks) * 100, 2)

    data = {'Total Number of tasks, ': total_tasks, 'Completed tasks, ': completed_tasks,
            'Uncompleted tasks, ': uncompleted_tasks, 'tasks overdue, ': overdue,
            'Uncompleted tasks %, ': uncompleted_percent, 'Overdue tasks %, ': overdue_percent}

    # Write the data into the overview file
    with open('task_overview.txt', 'w', encoding='utf-8') as overview_file:
        for keys, values in data.items():
            overview_file.write(f'{keys}{values}\n')


# The user_overview function generates a 'user_overview.txt' file that stores the statistics of each user's task
def user_overview():
    count_users = 0

    global line
    global user_file

    # Count the total number of users
    with open('user.txt', 'r', encoding='utf-8') as user_file:
        for line in user_file:
            count_users += 1

    # Write the total number of tasks and users into the user overview file
    user_overview_file = open('user_overview.txt', 'w', encoding='utf-8')
    user_overview_file.write(f'Total Number of Users, {count_users}\n')
    user_overview_file.write(f'Total Number of Tasks, {total_tasks}\n')
    user_overview_file.write(f'\n')
    user_overview_file.close()

    with open('user.txt', 'r', encoding='utf-8') as user_file:
        global months
        import datetime

        for users in user_file:
            use = users.strip('\n').split(', ')[0]
            total_user_tasks = 0
            completed_tasks = 0
            uncompleted_tasks = 0
            overdue = 0

            with open('tasks.txt', 'r', encoding='utf-8') as task_stat:
                for tasks in task_stat:
                    if use == tasks.strip('\n').split(', ')[0]:
                        # Get the due date string
                        due_date = tasks.strip('\n').split(', ')[4]
                        # split into day, month and year
                        day, month, year = due_date.split(" ")[0], due_date.split(" ")[1], due_date.split(" ")[2]
                        # set the month in words to a matching month number in the dict
                        for mon in months.keys():
                            if mon == month:
                                month = months[mon]
                                break
                        # Convert the date string to a date object
                        overdue_date = datetime.date(int(year), int(month), int(day))

                        if tasks.strip('\n').split(', ')[0] == use:
                            total_user_tasks += 1
                        if (tasks.strip('\n').split(', ')[5] == 'Yes') and (tasks.strip('\n').split(', ')[0] == use):
                            completed_tasks += 1
                        elif (tasks.strip('\n').split(', ')[5] == 'No') and (date.today() >= overdue_date) \
                                and (tasks.strip('\n').split(', ')[0] == use):
                            overdue += 1
                        elif (tasks.strip('\n').split(', ')[5] == 'No') and (tasks.strip('\n').split(', ')[0] == use):
                            uncompleted_tasks += 1

                # If they have been assigned 0 tasks divide by 1 to avoid zero division error
                if total_user_tasks == 0:
                    uncompleted_percent = round((uncompleted_tasks / 1) * 100, 2)
                    overdue_percent = round((overdue / 1) * 100, 2)
                    completed_percent = round((completed_tasks / 1) * 100, 2)
                    user_task_percent = round((total_user_tasks / total_tasks) * 100, 2)

                else:
                    # Calculate the following
                    uncompleted_percent = round((uncompleted_tasks / total_user_tasks) * 100, 2)
                    overdue_percent = round((overdue / total_user_tasks) * 100, 2)
                    completed_percent = round((completed_tasks / total_user_tasks) * 100, 2)
                    user_task_percent = round((total_user_tasks / total_tasks) * 100, 2)

                # Put the data into a dictionary
                data = {'User, ': use, f'Total number of {use} tasks, ': total_user_tasks,
                        'Completed tasks %, ': completed_percent, 'Uncompleted tasks %, ': uncompleted_percent,
                        'Overdue tasks %, ': overdue_percent, '% Of tasks assigned, ': user_task_percent}

                # Write the data into the overview file,
                with open('user_overview.txt', 'a', encoding='utf-8') as user_overview_file:
                    for keys, values in data.items():
                        user_overview_file.write(f'{keys}{values}\n')
                    user_overview_file.write(f'\n')


def main_menu():
    # if user is admin display and extra option
    if user == 'admin':
        print("r - register user \na - add task \nva - view all tasks \nvm - view my tasks "
              "\ngr - generate reports \nds - display statistics \ne - exit")
    else:
        print("r - register user \na - add task \nva - view all tasks \nvm - view my tasks \ne - exit")

    choice = input()

    # REGISTER NEW USER
    if choice == 'r':
        if user == 'admin':
            reg_user()
        else:
            print("Sorry only the admin is allow to register new users")
        print()
        main_menu()

    # ADD A NEW TASK
    elif choice == 'a':
        add_task()
        print("New task had been added")
        print()
        main_menu()

    # VIEW ALL TASKS
    elif choice == 'va':
        # Create a list of outputs
        outputs = ['Assigned to:', 'Task:', 'Task Description:', 'Date assigned:', 'Due date:', 'Task complete?']
        view_all(outputs)
        print()
        main_menu()

    # VIEW ALL MY TASKS
    elif choice == 'vm':
        view_mine(user)
        if user_found:
            print("\nPlease enter the number of the task you want to choose or Enter -1 to return to main menu ")
            global task_choice
            task_choice = int(input())

            while task_choice not in range(1, count + 1):
                # Return to main menu
                if task_choice == -1:
                    print()
                    main_menu()
                    break
                else:
                    print("Please enter a valid task number or Enter -1 to return to main menu")
                    task_choice = int(input())

            else:
                print(f"\nm - mark task {task_choice} as complete \ned - edit task {task_choice}")
                intent = input()

                # Mark task as complete
                if intent == 'm':
                    mark_task_complete()
                    print(f"task {task_choice} has been marked as complete")

                    print()
                    main_menu()

                # Edit task
                elif intent == 'ed':
                    if can_be_edited():
                        print(f"\nas - reassign task {task_choice} \ndt - edit task {task_choice} due date")
                        edit_choice = input()
                        # Reassign task
                        if edit_choice == 'as':
                            reassigned = input("Enter the name of the person you want to reassign the task to:\n")
                            edit_task_reassign(reassigned)
                            print(f"task {task_choice} has been reassigned to {reassigned}")

                        # Change task due date
                        elif edit_choice == "dt":
                            new_date = input("Enter the new due date:\n")
                            edit_task_date(new_date)
                            print(f"task {task_choice}'s due date has been changed")

                    else:
                        print("\nSorry, task cannot be edited. It's been completed")

                    print()
                    main_menu()

    # GENERATE REPORTS
    elif choice == 'gr':
        # Check if it's the admin accessing the statistics
        if user != 'admin':
            print("\nInvalid input")

        else:
            task_overview()
            user_overview()
            print("Reports have been generated")

        print()
        main_menu()

    # DISPLAY STATISTICS
    elif choice == 'ds':
        # Check if it's the admin accessing the statistics
        if user != 'admin':
            print("\nInvalid input")

        else:
            global line
            global user_file
            task_overview()
            user_overview()
            print("TASK OVERVIEW")
            print("===================================================")

            # Display the task overview data
            with open('task_overview.txt', 'r', encoding='utf-8') as task_overview_file:
                for line in task_overview_file:
                    title = line.split(', ')[0]
                    print(f"{title.ljust(40)} {str(line.split(', ')[1])}")

            # Display the user overview data
            with open('user_overview.txt', 'r', encoding='utf-8') as user_overview_file:
                print("\n USER OVERVIEW")
                print("===================================================")
                for line in user_overview_file:
                    if line == "\n":
                        print("--------------------------------------------------------------")
                    else:
                        title = line.split(', ')[0]
                        print(f"{title.ljust(40)} {str(line.split(', ')[1])}")

        main_menu()

    # EXIT PROGRAM
    elif choice == 'e':
        # Learnt how to use the sys module to exit a program here
        # https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
        import sys
        sys.exit("\nExiting.............\nThank you for using the task manager")

    else:
        print("\nInvalid input")

        main_menu()


# =============================================================================================== #

# Request for login details
user = input("Enter Username:\n")
password = input("Enter password:\n")

# Create a login control variable
access_gained = False

# Validate login details
with open('user.txt', 'r+', encoding='utf-8') as users_file:
    for lines in users_file:
        if (lines.strip('\n').split(', ')[0] == user) and (lines.strip('\n').split(', ')[1] == password):
            access_gained = True

# Keep asking for valid username and password if wrong
while not access_gained:
    print("\nError, please enter a valid username and/password\n")

    user = input("Enter Username:\n")
    password = input("Enter password:\n")

    with open('user.txt', 'r+', encoding='utf-8') as user_file:
        for line in user_file:
            if (line.strip('\n').split(', ')[0] == user) and (line.strip('\n').split(', ')[1] == password):
                access_gained = True

# Allow access if username and password is correct
if access_gained:
    print("\nPlease select one of the following options:")

    main_menu()
