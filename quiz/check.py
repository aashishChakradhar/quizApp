import re
def valid_email(email): # standard email format
    pattern = r'^[^\d][\w\.-]+@[^\W_]+\.[a-zA-Z]+$'
    # Check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False

def valid_name(name): #contains only alphabets
    pattern = r'^[a-zA-Z]*$'
    if re.match(pattern, name):
        return True
    else:
        return False

def valid_username(username): # contain combination on letters and numbers
# always begins with alphabets
    pattern = r'^[^\d][\w\.-]*$'
    if re.match(pattern, username):
        return True
    else:
        return False

def validate_phone(number): #contains phone number as per nepali system
    pattern = r'^9[7-8][0-9]{8}$'
    if re.match(pattern, number):
        return True
    else:
        return False