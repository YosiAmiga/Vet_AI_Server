from flask import Flask
from flask_cors import CORS
from src.routes.user_routes import user_bp
from src.routes.pet_routes import pet_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(pet_bp)
CORS(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
