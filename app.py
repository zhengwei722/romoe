from applications import create_app
from flask_cors import CORS
app = create_app()
cors = CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run('0.0.0.0', 5010)
