FROM python
MAINTAINER alkersh.omar@pm.me

WORKDIR /django # requires a volume to be connected this location with the django project
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn --bind 0.0.0.0:8000 myproject.wsgi