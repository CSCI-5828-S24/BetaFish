FROM python:3.9-alpine
LABEL MAINTAINER="jogo1537@colorado.edu"

COPY src ./src

EXPOSE 5000

RUN pip3 install --upgrade redis jsonpickle requests flask flask_cors
WORKDIR /src
CMD ["python3", "flask-server.py"]