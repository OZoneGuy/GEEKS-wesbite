FROM python
MAINTAINER alkersh.omar@pm.me

WORKDIR /django

CMD pip install --no-cache-dir -r requirements.txt; gunicorn --bind 0.0.0.0:8000 geeks_website.wsgi