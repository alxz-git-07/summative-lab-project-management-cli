import argparse
import json
import os
from tabulate import tabulate
from lib.models import Task, User, Project


DB_FILE='database.json'
'''
load db.json file(storage)
 '''
def load_db():
    if not os.path.exists(DB_FILE):
        return{'users':{},'projects':{},'user_projects':{},'project_tasks':{}}
    with open(DB_FILE,'r') as file:
        return json.load(file)
    
def save_db(data):
    with open(DB_FILE,'w')as file:
        json.dump(data,file,indent=4)

'''
methods(CLI functions)
'''
def add_user(args):
    db=load_db()
    if args.email in db['users']:
        print(f'User with {args.email} already exists')
        return
    try: 
         user=User(args.name,args.email)
         db['users'][args.email]=user.to_dict()
         db['user_projects'][args.email]=[]
         save_db(db)
         print(f"Successfully added User'{user.name}' ")
    except ValueError as err:
        print(f'Validation error: {err}')

def view_users(args):
    db=load_db()
    if not db['users']:
        print('No users found')
        return
    
    table_data = []
    for email, info in db["users"].items():
        table_data.append([info["name"], email])
    
    # 2. Define your table headers
    headers = ["Name", "Email Address"]
    
    # 3. Print using tabulate
    print("\n=== SYSTEM USERS ===")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def update_user(args):
    db=load_db()
    if args.email not in db['users']:
        print(f'Sorry:user{args.email} not found')
        return
    if args.name:
        db['users'][args.email]['name']=args.name
    save_db(db)
    print(f'User {args.email} updated successfully')

def add_project(args):
    db=load_db()
    if args.user_email not in db['users']:
        print(f'User {args.user_email} does not exist')
        return
    if args.title in db['projects']:
        print(f'project {args.title} already exists')
        return
    try:
        project=Project(args.title,args.description,args.due_date)
        db['projects'][args.title]=project.to_dict()
        db['user_projects'][args.user_email].append(args.title)
        db['project_tasks'][args.title]=[]
        save_db(db)
        print(f'Project {args.title} successfully assigned to {args.user_email}')

    except ValueError as err:
        print(f'Validation error: {err}')

def view_projects(args):
    db=load_db()
    if args.user_email not in db['user_projects']:
        print(f'Assigned user {args.user_email} not found')
        return
    
    projects=db['projects']
    if not projects:
        print(f'No projects found inside user {args.user_email}')
        return
    table_rows = []

    
    for title, info in db['projects'].items():
        assigned_user = next(
            (user_email for user_email, titles_list in db['user_projects'].items() if title in titles_list), 
            "Unassigned"
        )
        
    
        table_rows.append([title, info['description'], info['due_date'], assigned_user])

    
    headers = ["Project Title", "Description", "Due Date", "Assigned To"]

    
    print(tabulate(table_rows, headers=headers, tablefmt="fancy_grid"))

def add_task(args):
    db=load_db()
    if args.project not in db['projects']:
        print(f'Project{args.project} does not exist')
        return
    if args.assigned_to not in db['users']:
        print(f'Assigned user {args.assigned_to} does not exist')
        return
    task=Task(args.title,assigned_to=args.assigned_to)
    db['project_tasks'][args.project].append(task.to_dict())
    save_db(db)
    print(f'Task {args.title} successfully added to project {args.project}')

def view_tasks(args):
    db=load_db()
    if args.project not in db['project_tasks']:
        print(f'Project {args.project} not found')
        return
    
    tasks=db['project_tasks'][args.project]
    if not tasks:
        print(f'No tasks found inside project {args.project}')
        return
    for task in tasks:
        print(f'Completed :{task['completed']} title: {task['title']} Assigned to:{task['assigned_to']}')




def complete_task(args):
    project=Project.all_projects.get(args.project)
    if project:
        for task in project.tasks():
            if task ==args.title:
                task.complete()
                return
            print('Task not found')
        else:
            print('User not found')
    


def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI Tool")
    subparsers = parser.add_subparsers(dest='entity',help='stores the user\'s chosen command')

    # user sub-commands
    user_parser = subparsers.add_parser("user", help="Add a user")
    user_action=user_parser.add_subparsers(dest='action')

    #add user
    user_add=user_action.add_parser('add',help='Add a new user')
    user_add.add_argument('--name',help='Users full name')
    user_add.add_argument('--email',help='Users email address')
    user_add.set_defaults(func=add_user)

    #view users
    view_user=user_action.add_parser('view',help='View all users')
    view_user.set_defaults(func=view_users)

    #update user
    user_update=user_action.add_parser('update',help='modify an existing user')
    user_update.add_argument('--email',help='email of target user')
    user_update.add_argument('--name',help='new name value')
    user_update.set_defaults(func=update_user)

    # Subparser for complete-task
    complete_parser = user_action.add_parser("complete-task", help="Mark a user's task as complete")
    complete_parser.add_argument("--project",help='project to mark as complete')
    complete_parser.add_argument("--title",help='project title')
    complete_parser.set_defaults(func=complete_task)

    #project sub commands
    project_parser=subparsers.add_parser('project',help='Manage projects')
    project_action=project_parser.add_subparsers(dest='actions')

    #Subpursers for add-project
    project_add=project_action.add_parser('add',help='Add a project to a user')
    project_add.add_argument('--title')
    project_add.add_argument('--description')
    project_add.add_argument('--due_date')
    project_add.add_argument('--user_email')
    project_add.set_defaults(func=add_project)

    #view project
    project_view=project_action.add_parser('view',help="View user specific projects")
    project_view.add_argument('--user_email',help='user\'s email to access user specific projects')
    project_view.set_defaults(func=view_projects)

    #Task subcommands
    task_parser=subparsers.add_parser('task',help='manage tasks')
    task_action=task_parser.add_subparsers(dest='actions')

    #Add tasks
    task_add=task_action.add_parser('add',help='Add tasks')
    task_add.add_argument('--title',help='Task title')
    task_add.add_argument('--project',help='project to which the task belongs')
    task_add.add_argument('--assigned_to',help='target email for the user executing the task')
    task_add.set_defaults(func=add_task)

    #task view
    task_view=task_action.add_parser('view',help='View project specific tasks')
    task_view.add_argument('--project',help='target project')
    task_view.set_defaults(func=view_tasks)



    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__=='__main__':
    main()

