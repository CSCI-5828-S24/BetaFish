FROM python:3.9-alpine
LABEL MAINTAINER="jogo1537@colorado.edu"

COPY flask-backend/src ./flask-backend/src
COPY react-frontend/build ./react-frontend/build


EXPOSE 5000

RUN pip3 install --upgrade redis jsonpickle requests flask flask_cors flask-mysqldb
WORKDIR /flask-backend/src
CMD ["python3", "flask_server.py"]