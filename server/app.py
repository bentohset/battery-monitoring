from src import create_app, create_database
from src.routes import *

app = create_app()

@app.route("/")
def hello():
    return "hello backend"

if __name__ == '__main__':
    app.run(debug=True)