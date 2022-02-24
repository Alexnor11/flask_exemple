from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from jsonschema import validate, ValidationError

from schema import USER_CREATE

app = Flask(__name__)

# Подключаемся к БД
PG_DSN = 'postgresql://admin:1234@127.0.0.1:5431/flask_test'
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=PG_DSN)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Создание модели
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))


# Создание Views
class UserViews(MethodView):

    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user is not None:
            return jsonify({'email': user.email, 'username': user.username})
        else:
            response = jsonify({'error': 'not found'})
            response.status_code = 404
            return response

    def post(self):
        try:
            validate(request.json, USER_CREATE)
        except ValidationError as er:
            response = jsonify({
                'error': 'not valid',
                'description': er.message,
            })
            response.status_code = 400
            return response
        new_user = UserModel(**request.json)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                'id': new_user.id,
                'email': new_user.email,
            }
        )


@app.route('/health/', methods=['GET', ])
def health():
    return jsonify({'status': 'OK'})


# app.add_url_rule('/health/', view_func=health, methods=['GET', ])
app.add_url_rule('/users/<int:user_id>', view_func=UserViews.as_view('users_get'), methods=['GET', ])
app.add_url_rule('/users/', view_func=UserViews.as_view('users_create'), methods=['POST', ])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
