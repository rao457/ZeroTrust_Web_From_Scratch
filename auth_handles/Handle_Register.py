from urllib.parse import unquote_plus
from app.Response import make_response
from app.Database import save_user
from app.auth_utils import hash_passwd

def handle_register(client_socket, body):
   
    reg_data = {}
    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            reg_data[key] = unquote_plus(value)
    username = reg_data.get("username")
    email = reg_data.get("email")
    password = reg_data.get("password")
    
    if not username or not email or not password:
        response = make_response(400, "<h3>Missing credentials</h3>")
        # client_socket.sendall(response)
        # client_socket.close()
        return response
    
    hashed_password = hash_passwd(password)
    save_user(username, email, hashed_password)
    print("👤 User saved in database.")
    response = (
        "HTTP/1.1 302 Found\r\n"
        "Location: /login\r\n"
        "Content-Length: 0\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8")
    # client_socket.sendall(response)
    # client_socket.close()
    
    return response

    
