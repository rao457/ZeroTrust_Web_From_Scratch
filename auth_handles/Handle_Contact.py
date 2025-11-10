from app.Database import save_contact
from urllib.parse import unquote_plus

def handle_contact(client_socket, body):
    cntct_data = {}
    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            cntct_data[key] = unquote_plus(value)
    
    name = cntct_data.get("name")
    email = cntct_data.get("email")
    message = cntct_data.get("message")
    
    save_contact(name, email, message)
    
    response  = (
        "HTTP/1.1 302 Found\r\n"
        "Location: /\r\n"
        "Content-Length: 0\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8")
    client_socket.sendall(response)
    client_socket.close()
    return