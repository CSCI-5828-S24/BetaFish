FROM python:3.9-alpine
LABEL MAINTAINER="jogo1537@colorado.edu"

COPY flask-backend ./flask-backend
COPY react-frontend/build ./react-frontend/build

EXPOSE 5000

RUN pip3 install --upgrade -r ./flask-backend/requirements.txt
WORKDIR /flask-backend/src
CMD ["python3", "flask_server.py"]