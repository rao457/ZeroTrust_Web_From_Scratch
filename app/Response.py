import mimetypes

def make_response(status_code: int, body, content_type: str = "text/html"):
    status_messages = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Server Error"
    }
    
    status_message = status_messages.get(status_code, "Unknown Status")

    # If body is str, encode it
    if isinstance(body, str):
        body = body.encode("utf-8")

    headers = f"HTTP/1.1 {status_code} {status_message}\r\n"
    headers += f"Content-Type: {content_type}\r\n"
    headers += f"Content-Length: {len(body)}\r\n"
    headers += "Connection: close\r\n"
    headers += "\r\n"

    return headers.encode() + body



def guess_mime_type(filepath: str) -> str:
    content_type, _ = mimetypes.guess_type(filepath)
    return content_type or "application/octet-stream"
