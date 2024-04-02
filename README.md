# BetaFish
Group 12: Emily Parker, Ranajit Roy, Jonathan Gorman

# Instructions

Below are the instruction run the we app locally on an linux/ubuntu platform

Install the below packages before proceeding -
1. Python3
2. Python packages: redis jsonpickle requests flask flask_cors
    > pip3 install --upgrade redis jsonpickle requests flask flask_cors
3. Node.js 20.x lts


FIrst clone the repository

> git clone \<repo-clone-url\>

then to build the app, run the commands below in the cloned directory -

```
npm --prefix ./react-frontend/ ci
npm --prefix ./react-frontend/ build
```

Now there are two options:
* run locally
* run with a docker image


## Run locally

> python3 flask-backend/src/flask-server.pyv

## Run on Docker

In order to run on a docker image, run the below commands:

```
docker build -t web-app .
docker run -p5000:5000 web-app
```

Now, the web page should be accessible on port 5000 on localhost