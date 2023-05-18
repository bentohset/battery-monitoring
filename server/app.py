from src import create_app

app = create_app()

@app.route("/")
def hello():
    return "hello backend"

if __name__ == '__main__':
    app.run(debug=True)