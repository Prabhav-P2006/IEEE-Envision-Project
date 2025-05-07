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
