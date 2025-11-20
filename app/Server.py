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
from app.session_repo import get_user_by_session

TEMPLATE_DIRS = 'templates'
STATIC_DIRS = 'static/'

# REQUIRED FOR RENDER
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8080))

def handle_client(client_socket, client_address):
    filepath = ""
    print(f"📩 Connection from {client_address}")
    
    try:
        request = client_socket.recv(1024).decode('utf-8', errors="ignore")
        print("-----HTTP REQUEST------")
        print(request)
        print("-----------------------")
        
        method, path, header, body = parse_http_request(request)
        if not method or not path:
            response = make_response(400, "<h1>Bad Request</h1>")
            client_socket.sendall(response)
            return

        user = None
        cookie_header = header.get("Cookie")
        
        if cookie_header:
            cookies = dict(c.split("=", 1) for c in cookie_header.split("; ") if "=" in c)
            session_id = cookies.get("session_id")
            if session_id:
                user = get_user_by_session(session_id)
                print(f"👤 {user}")
        else:
            session_id = None

        if path == "/":
            filepath = os.path.join(TEMPLATE_DIRS, 'home.html')

        elif path == "/contact" and method == "POST":
            response = handle_contact(client_socket, body)
            client_socket.sendall(response)
            return

        elif path == "/register" and method == "GET":
            filepath = os.path.join(TEMPLATE_DIRS, 'register.html')

        elif path == "/register" and method == "POST":
            response = handle_register(client_socket, body)
            client_socket.sendall(response)
            return

        elif path == "/login" and method == "GET":
            filepath = os.path.join(TEMPLATE_DIRS, 'login.html')

        elif path == "/login" and method == "POST":
            response = handle_login(client_socket, body)
            client_socket.sendall(response)
            return

        elif path.startswith("/static/"):
            filepath = path.lstrip("/")

        elif path.startswith("/logout"):
            print("Entered logout block")
            from app.session_repo import delete_session
            if session_id:
                delete_session(session_id)

            response  = b"HTTP/1.1 302 Found\r\n"
            response += b"Location: /\r\n"
            response += b"Set-Cookie: session_id=; Max-Age=0; Path=/; HttpOnly\r\n"
            response += b"Content-Length: 0\r\n"
            response += b"Connection: close\r\n\r\n"

            client_socket.sendall(response)
            return

        else:
            if "?" in path:
                path, query = path.split("?", 1)
            filepath = os.path.join(TEMPLATE_DIRS, path.lstrip("/") + ".html")

        binary = not filepath.endswith(".html")
        body = load_file(filepath, binary=binary)
        
        if body is None:
            response = make_response(404, "<h1>404 Not Found</h1>")
        else:
            content_type = guess_mime_type(filepath)
            if not binary:
                if isinstance(body, bytes):
                    body = body.decode()

                replacement = (
                    f"<a href='/logout'>Logout</a> | Welcome {user}"
                    if user else
                    "<a href='/login'>Login</a> <a href='/register'>Sign Up</a>"
                )
                body = body.replace("{{ auth_links }}", replacement)
                body = body.encode()

            response = make_response(200, body, content_type)

        client_socket.sendall(response)

    except Exception as e:
        print(f"⚠️ Error: {e}")
        response = make_response(500, "<h1>Internal Server Error</h1>")
        client_socket.sendall(response)

    finally:
        client_socket.close()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"🚀 Server running on {HOST}:{PORT}")
    init_db()
    print("📦 Database ready.")

    while True:
        client_socket, client_addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_addr)).start()
