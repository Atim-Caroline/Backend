@echo off
echo Starting Client Nest Deployment...

REM Activate virtual environment
call venv\Scripts\activate

REM Install/upgrade production dependencies
pip install -r requirements.txt

REM Collect static files
python manage.py collectstatic --noinput

REM Apply database migrations
python manage.py migrate --noinput

REM Start the production server
set DJANGO_SETTINGS_MODULE=social_insights.settings_prod
python deploy.py 