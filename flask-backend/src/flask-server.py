from flask import Flask, request, Response
from flask_cors import CORS
import jsonpickle
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200"])

"""
Health check endpoint for getting status of api
"""
@app.route('/health', methods=["GET"])
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

def main():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()