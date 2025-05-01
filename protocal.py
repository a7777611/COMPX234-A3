def valid_request(request):
    # use maxsplit to ensure the value of key
    parts = request.strip().split(maxsplit=1)
    
    if len(parts) < 2:
        return False, "Invalid request format"
    
    operation = parts[0]
    remaining = parts[1]

    if operation not in ['PUT','GET','READ']:
        return False, "Invalid operation"
    
    if operation in ['GET', 'READ']:
        # for GET and READ operation, the remaining part is the key
        key = remaining
        if len(key) > 999:
            return False, "Key too long"
    
    elif operation == 'PUT':
        key_value = remaining.split(maxsplit=1)
        key,value = key_value

        if len(key_value) < 2:
            return False, "PUT needs a value"
        if len(key) or len(value) > 999:
            return False,"key or value is too long"
    
    return True, ""

# NNN R/G/P k [v]
def format_requeset(request):
    valid, msg = valid_request(request)
    if not valid:
        raise ValueError(msg)
    
    parts = request.strip().split(maxsplit=1)

    operation = parts[0]
    remaining = parts[1]

    # three operations
    if operation == 'GET':
        op = 'G'
        formatted_request = f"{op} {remaining}"         

    elif operation == 'READ':
        op = 'R'
        formatted_request = f"{op} {remaining}"
    
    else: 
        key_value = remaining.split(maxsplit=1)
        key,value = key_value
        op = 'P'
        formatted_request = f"{op} {key} {value}"

    size = 4 + len(formatted_request) # 3 for size digits and 1 for space
    # check the total size
    if size > 999:
        raise ValueError("Request size exceeds maximum limit")
    return f"{size:03d} {formatted_request}" 

def parse_response(response):
    parts = response.split(maxsplit=1)
    if len(parts) <2:
        return "Invalid response format"
    return parts[1]



