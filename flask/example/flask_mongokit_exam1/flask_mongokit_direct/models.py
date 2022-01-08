from flask_mongokit_direct.flask_mongokit_direct import connection
from mongokit import Document

def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception("%s must be at most %s characters long"% length)
    return validate

class User(Document):
    structure = {
        "name": str,
        "email": str,
    }

    validators = {
        "name": max_length(50),
        "email": max_length(120)
    }

    use_dot_notation = True

    def __repr__(self):
        return f"<User {self.name}>"

# register the User document with our current connection
connection.register([User])
