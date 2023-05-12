from flask import Flask
from flask_cors import CORS, cross_origin
import datetime

app = Flask(__name__)
cors = CORS(app)

x = datetime.datetime.now()

@app.route('/')
def hello():
    return {
        "Name":"Test", 
        "Date":"Due", 
    }

if __name__ == '__main__':
    app.run(debug=True)