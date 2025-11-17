from urllib.parse import unquote_plus
from app.Response import make_response
from app.Database import get_user
from app.auth_utils import check_password
from app.session_repo import create_session

def handle_login(client_socket, body):
    # Step 1: Parse form data
    log_data = {}
    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            log_data[key] = unquote_plus(value)

    username = log_data.get("username")
    password = log_data.get("password")

    # Step 2: Validate fields
    if not username or not password:
        return make_response(400, "<h3>User is not registered</h3>")

    # Step 3: Get user from DB
    user = get_user(username)
    if not user:
        response = (
            "HTTP/1.1 302 Found\r\n"
            "Location: /register\r\n"
            "Content-Length: 0\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8")
        return response

    stored_username, email, hashed_password = user

    # Step 4: Verify credentials
    if not check_password(password, hashed_password):
        return make_response(401, "<h3>Incorrect Credentials</h3>")

    # Step 5: Create session
    session_id = create_session(stored_username)

    # Step 6: Build redirect with Set-Cookie *before* blank line
    response = (
        "HTTP/1.1 302 Found\r\n"
        "Location: /\r\n"
        f"Set-Cookie: session_id={session_id}; HttpOnly\r\n"
        "Content-Length: 0\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8")

    return response
