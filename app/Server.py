import os 
import socket 
import threading
from app.Utils import load_file
from app.Parser import parse_http_request
from app.Response import make_response, guess_mime_type
from app.Database import init_db, save_contact, save_user, get_user
from urllib.parse import unquote_plus
from app.auth_utils import hash_passwd, check_password
from auth_handles.Handle_Login import handle_login
from auth_handles.Handle_Register import handle_register
from auth_handles.Handle_Contact import handle_contact
# Constact Dirs addresses

TEMPLATE_DIRS =   'templates'
STATIC_DIRS = 'static/'
HOST = '127.0.0.1'
PORT = 8080

def handle_client(client_socket, client_address):
    print(f"📩 Connection from {client_address}")
    
    try:
        request = client_socket.recv(1024).decode('utf-8', errors="ignore")
        print("-----HTTP REQUEST------")
        print(request)
        print("-----------------------")
        
        method, path, header, body= parse_http_request(request)
        if not method or not path:
            response = make_response(400, "<h1>Bad Request 4000</h1>")
            client_socket.sendall(response)
            return
        print(f"👉 Method: {method}, Path: {path}")
        
        if path == "/":
            filepath = os.path.join(TEMPLATE_DIRS, 'home.html') 
        
        # HANDLING CONTACT FORM
        
        elif path == "/contact" and method == "POST":
            handle_contact(client_socket, body)
            
        # HANDLING THE REGISTER ROUTE
        
        elif path == '/register' and method == "GET":
            filepath = os.path.join(TEMPLATE_DIRS, 'register.html')
        elif path == '/register' and method == "POST":
            handle_register(client_socket, body)
            
        # HANDLING THE LOGIN ROUTE
        elif path == "/login" and method == "GET":
            filepath = os.path.join(TEMPLATE_DIRS, 'login.html')             
        elif path == "/login" and method == "POST":
            handle_login(client_socket, body)
        
                   
        elif path.startswith("/static/"):
            filepath = path.lstrip("/")
        else:
            if "?" in path:
                path, query = path.split("?", 1)
            else:
                query = ""
            filepath = os.path.join(TEMPLATE_DIRS, path.lstrip("/")+".html")
            
        binary = not filepath.endswith(".html")
        body = load_file(filepath, binary=binary)
        
        if body is None:
            response = make_response(404, "<h1>Page not found</h1>")
        else:
            content_type = guess_mime_type(filepath)
            response = make_response(200, body, content_type)
        client_socket.sendall(response)
        
    except Exception as e:
        print(f"⚠️ Error handling client {client_address}: {e}")
        error_response = make_response(500, "<h1>500 Internal Server Error</h1>")
        client_socket.sendall(error_response)
    finally:
        client_socket.close()
        
# Main Server
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"🚀 Server is running on http://{HOST}:{PORT}")
    init_db()
    print("📦 Database ready!")
    while True:
        client_socket, client_addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()
