from flask import (
    Flask
)

from sqlalchemy.exc import SQLAlchemyError
from orm.data_base import init_app
from flask import (
    request,
    make_response
)

from sqlalchemy.orm import Session
from models.user import User
from orm.data_base import db


def create_app():
    app_flask = Flask(__name__)
    init_app(app_flask)
    return app_flask


app = create_app()


@app.route('/insert', methods=['POST'])
def api_insert():
    data = request.get_json()
    email = data['email']
    username = data['username']

    user = User(email, username)

    try:
        _session = Session(db.engine)
        _session.add(user)
        _session.commit()
        _session.close()

        return make_response({'sucess': 'Usuário criado!'}, 200)
    except SQLAlchemyError as err:
        return make_response({'error': f'Erro ao criar usuário {err.__cause__}!'}, 400)


@app.route('/edit', methods=['POST'])
def api_edit():
    data = request.get_json()
    pk = data['id']
    email = data['email']
    username = data['username']

    try:
        _session = Session(db.engine)
        user = _session.query(User).filter(User.id == pk).first()
        if user:
            user.update(
                {"email": email, "username": username}
            )
            _session.commit()
            _session.close()
        else:
            return make_response({'sucess': f'Id Usuário não encontrado!'}, 404)

        return make_response({'sucess': f'Usuário editado!'}, 200)
    except SQLAlchemyError as err:
        return make_response({'error': f'Erro ao editar usuário! {err.__cause__}'}, 400)


@app.route('/delete', methods=['POST'])
def api_delete():
    data = request.get_json()
    pk = data['id']

    try:
        _session = Session(db.engine)
        user = _session.query(User).filter(User.id == pk).first()
        if user:
            _session.commit()
            _session.close()
            return make_response({'sucess': f'Usuário deletado!'}, 200)
        else:
            return make_response({'sucess': f'Id Usuário não encontrado!'}, 404)

    except SQLAlchemyError as err:
        return make_response({'error': f'Erro ao deletar usuário! {err.__cause__}'}, 400)


@app.route('/list', methods=['GET'])
def api_list():
    try:
        _session = Session(db.engine)
        users = _session.query(User).all()
        _session.close()
        users_list = list()

        for user in users:
            user_username = user.username
            user_email = user.email
            user_id = user.id
            dict_user = {
                "email": user_email,
                "name": user_username,
                "id": user_id
            }
            users_list.append(dict_user)

        return make_response({'Usuários': users_list}, 200)

    except SQLAlchemyError as err:
        return make_response({'error': f'Erro ao listar usuários! {err.__cause__}'}, 400)


if __name__ == '__main__':
    app = create_app()
    app.run()
