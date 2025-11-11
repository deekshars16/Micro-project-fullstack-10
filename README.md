# bloodproj

Small Django project for managing blood donors and requests.

Quick start (using the included virtualenv):

1. Activate the virtualenv (PowerShell):
   & "bloodenv\Scripts\Activate.ps1"

   Or (cmd.exe):
   "bloodenv\Scripts\activate.bat"

2. Run migrations:
   "bloodenv\Scripts\python.exe" "bloodproj\manage.py" migrate

3. Run the dev server (cmd.exe):
   "bloodenv\Scripts\python.exe" "bloodproj\manage.py" runserver

Notes:
- `phonenumber_field` is listed in `INSTALLED_APPS`.
- Static files directory `bloodproj/static` was created to satisfy `STATICFILES_DIRS`.
