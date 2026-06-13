import re
from datetime import datetime

class User:
    
    def __init__(self, name,email):
        self.name=name
        self.email=email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # Regular expression pattern for basic email structure validation
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise ValueError(f"Invalid format: '{value}' is not a valid email address.")
        self._email = value

    
    def to_dict(self):
        return{'name':self.name, 'email':self.email}
    
    def __repr__(self):
        return f"User(Name: '{self.name}', Email: '{self.email}')"
   


class Project:
    def __init__(self,title,description,due_date):
        self.title=title
        self.description=description
        self.due_date=due_date

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        # Validate that string matches exactly YYYY-MM-DD
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid format: '{value}' must use the YYYY-MM-DD template.")
        self._due_date = value
        
    def to_dict(self):
        return{'title':self.title,'description':self.description,'due_date':self.due_date}
    
    def __repr__(self):
        return f"Project(Title: '{self.title}', Due: {self.due_date})"



class Task:
    all_tasks={'tasks':[]}
    def __init__(self, title,completed=False,assigned_to=None):
        self.title=title
        self.completed=completed
        self.assigned_to=assigned_to

    def to_dict(self):
        return{'title':self.title,'completed':self.completed,'assigned_to':self.assigned_to}
           

    def complete(self):
        self.completed=True
        print(f"Task'{self.title}'marked as complete")




    
        
    

    



        
    


