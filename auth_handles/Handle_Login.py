from urllib.parse import unquote_plus
from app.Response import make_response
from app.Database import get_user
from app.auth_utils import check_password
def handle_login(client_socket, body):
    log_data = {}
    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            log_data[key] = unquote_plus(value)
        username = log_data("username")
        password = log_data("password")
        
        if not username or not password:
            response = make_response(400, "<h3>User is not registered</h3>")
            client_socket.sendall(response)
            client_socket.close()
            return
        user = get_user(username)
        
        if not user:
            response = (
                "HTTP/1.1 302 Found\r\n"
                "Location: /register\r\n"
                "Content-Length: 0\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode("utf-8")
            client_socket.sendall(response)
            client_socket.close()
            return
        st_username, email, hashed_password = user
        if check_password(password, hashed_password):
            response = (
                "HTTP/1.1 302 Found\r\n"
                "Location: /welcome.html\r\n"
                "Content-Length: 0\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode("utf-8")
            client_socket.sendall(response)
            client_socket.close()
            return
        else:
            response = make_response(401, "<h3>Incorrect Credentials</h3>")
        client_socket.sendall(response)
        client_socket.close()
        return
        
    