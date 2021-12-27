import re 

def snake_case(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()