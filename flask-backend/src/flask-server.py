from flask import Flask, request, Response
from flask_cors import CORS
import jsonpickle
import os

app = Flask(__name__, static_folder="../../react-frontend/build", static_url_path='/')
CORS(app, origins=["*"])

"""
Hosting web pages from Flask itself
"""
@app.route('/')
def index():
    return app.send_static_file('index.html')

"""
Health check endpoint for getting status of api
"""
@app.route('/api/health', methods=["GET"])
def health():
    status = 200
    try:
        response = {
            'data' : True
        }
    except Exception as error:
        response = { 
            'error' : error 
        }
        status = 500
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=status, mimetype='application/json')

@app.route('/api/multiply/<int:x>/<int:y>', methods=["GET"])
def multiply(x, y):
    status = 200
    try:
        response = {
            'data' : x * y
        }
    except Exception as error:
        response = { 
            'error' : error 
        }
        status = 500
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=status, mimetype='application/json')
   

def main():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()