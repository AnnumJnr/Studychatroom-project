# Studychatroom-project
# Studychatroom-project

---

**This is a simple project made to understand the Django framework.**

## Getting Started

### Prerequisites
- Python 3.x installed
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AnnumJnr/Studychatroom-project.git
   cd Studychatroom-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. (Optional) Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the site at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Project Structure

- `manage.py`: Django project management script.
- `studymate/`: Django project configuration files (`settings.py`, `urls.py`, etc.).
- `base/`: Main Django app for chatroom logic.
- `templates/` and `static/`: HTML and static files.

---

## Notes

- The database file (`db.sqlite3`) is included for reference, but you should generate your own by running migrations.
- If you use environment variables, create a `.env` file and configure `settings.py` accordingly.
