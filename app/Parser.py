def parse_http_request(request:str):
    """
    Parses raw HTTP request and returns method, path, and headers.
    """
    try:
        
        if not request:
            return None, None, {}, ""
        parts = request.split("\r\n\r\n", 1)
        header_text = parts[0]
        body  = parts[1] if len(parts) > 1 else ""
        lines = header_text.split("\r\n")
        
        request_line = lines[0].split(" ")
        if len(request_line) < 2:
            return None, None, {}
        method = request_line[0]
        path = request_line[1]
        
        headers = {
            
        }
        for line in lines[1:]:
            if line == "":
                break
            
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        
        return method, path, headers, body
    except Exception as e:
        print(f"[Parser Error] {e}")
        return None, None, {}, ""