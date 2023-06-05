from flask import Flask
from flask_restful import Api
from flask_cors import CORS


from resources.Recommend_Competencies import Recommend_Competencies

app = Flask(__name__)


CORS(app, supports_credentials=True)
# app.config["PROPAGATE_EXCEPTIONS"] = True
# Setup the Flask-JWT-Extended extension
# app.secret_key = "sifi"  ## Change JWT secret key optionals
api = Api(app)
# jwt = JWTManager(app)
# mail = Mail(app)

api.add_resource(Recommend_Competencies, "/recommender")


# api.add_resource(ImageUpload, '/image')


@app.route("/")
def helloword():
    return "HELOO api"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
