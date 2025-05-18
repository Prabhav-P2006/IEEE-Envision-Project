## How to Setup-

### 1. Clone the Repo

```bash
git clone <repo-url>
cd <project-directory>
```

### 2. Create and Activate a Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

 `(venv)` should appear at the beginning of the prompt now.

### 3. Install PIP


```bash
pip install django
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

Server will now run at http://127.0.0.1:8000/



## Functionality of endpoints-

### 1. Functionality of the container list api endpoint
Get the list of containers and its specifications in json format

URL
http://127.0.0.1:8000/api/containers/
Method : GET

Response:

Success
HTTP Response : 200 OK

{
    "count": 2,
    "results": [
        {
            "id": "8e0c9f272202",
            "name": "test-container",
            "status": "exited",
            "image": "nginx:latest",
            "created": "2025-04-03T10:29:31.086534304Z"
        },
        {
            "id": "a1b22b9dce98",
            "name": "portainer",
            "status": "running",
            "image": "portainer/portainer:latest",
            "created": "2025-04-01T19:51:25.463538054Z"
        }
    ]
}
