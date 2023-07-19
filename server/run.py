"""Main process creating and running the application"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    print('run')
    app.run(debug=True)