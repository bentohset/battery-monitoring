from src import create_app
from flask import jsonify

app = create_app('config.DevelopmentConfig')  # change to ProductionConfig for prod

@app.route("/")
def hello():
    return jsonify({'message': 'hello backend'}), 200

if __name__ == '__main__':
    app.run(debug=True)