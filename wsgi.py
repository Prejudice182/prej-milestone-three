# Import our application constructor
from application import create_app

# Initialize application
app = create_app()

# If called directly, start server
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
