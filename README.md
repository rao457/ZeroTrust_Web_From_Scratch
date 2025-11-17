
# Web From Scratch (Project of Humble Tech)

A minimal web framework built from scratch using Python and raw sockets.  
Implements user authentication, contact forms, session management, and static file serving.

---

## Features

- User registration and login with hashed passwords  
- Session-based authentication using SQLite  
- Logout functionality with proper cookie handling  
- Contact form submission stored in the database  
- Static file serving (CSS, JS, images)  
- Basic templating with placeholder replacement (`{{ auth_links }}`)  
- Multi-threaded socket server

---

## Requirements

- Python 3.10+  
- SQLite3  

---

## Project Structure

```

project_root/
│
├─ app/
│   ├─ Database.py
│   ├─ Utils.py
│   ├─ Response.py
│   ├─ Parser.py
│   ├─ auth_utils.py
│   └─ session_repo.py
│
├─ auth_handles/
│   ├─ Handle_Login.py
│   ├─ Handle_Register.py
│   └─ Handle_Contact.py
│
├─ templates/
│   ├─ home.html
│   ├─ login.html
│   ├─ register.html
│   ├─ contact.html
│   └─ logout.html
│
├─ static/
│   └─ (CSS, JS, images)
│
├─ data/
│   └─ data.db
│
└─ server.py

````

---

## How to Run

1. Clone the repository:

```bash
git clone <your-repo-url>
cd web-from-scratch
````

2. Install Python dependencies (if any):

```bash
pip install -r requirements.txt
```

3. Initialize the database:

```python
from app.Database import init_db
init_db()
```

4. Start the server:

```bash
python server.py
```

5. Open your browser and visit:

```
http://127.0.0.1:8080
```

---

## Notes

* This is a learning project; **not production-ready**.
* For security: remove database files or credentials before sharing publicly.
* Supports only HTTP, not HTTPS.
* Cookies and sessions are stored in SQLite; no caching or session expiration yet.

---

## License

MIT License

```

---

I can also create a **polished `.gitignore` and folder structure** so your database and sensitive files are safe for public GitHub hosting.  

Do you want me to do that next?
```
