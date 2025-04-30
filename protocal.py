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
    
    return True

def format_requeset(request):
    parts = request.strip().split(maxsplit=1)

    operation = parts[0]
    remaining = parts[1]

    if operation == 'GET':
        op = 'G'
        requests = f"{op} {remaining}"         

    elif operation == 'READ':
        op = 'R'
        requests = f"{op} {remaining}"
    
    else: 
        key_value = remaining.split(maxsplit=1)
        key,value = key_value
        op = 'P'
        requests = f"{op} {key} {value}"

    size = len(requests) + 4 # 3 for size and 1 for space
    return f"{size:03d} {requests}" 

def parse_response(response):
    parts = response.split(maxsplit=1)
    if len(parts) <2:
        return "Invalid response format"
    return parts[1]



