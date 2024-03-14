from flask import Blueprint, render_template, request, jsonify, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import exc as SQLAlchemyError
from wtforms.validators import ValidationError
from werkzeug.security import generate_password_hash

from model.user import User
from config.db import db
from forms.user import UserForm
from services.generate_token import generate_token
from services.require_content_type import require_content_type

user:object = Blueprint('user', __name__)

@require_content_type('aplications/JSON')
@user.route('/api/user/create', methods=['GET', 'POST'])
def create_user():
    form:object = UserForm()
    if request.method == "GET":
        token = generate_token()
        return render_template('user_create.html', token=token)
    else:
        if form.validate_on_submit():
            
            user_by_doc_num = User.query.filter_by(document_number=form.document_number.data, doc_type_id=form.doc_type_id.data).first()

            email = User.query.filter_by(email=form.email.data).first()
            if user_by_doc_num:
                return jsonify({'error': 'Existe un usuario con el mismo número de documento'}), 400
            if email:
                return jsonify({'error': 'Existe un usuario con el mismo email'}), 400
            try:
                hashed_password = generate_password_hash(form.password.data)
                new_user:object = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    document_number=form.document_number.data,
                    email=form.email.data,
                    password=hashed_password,
                    role_id=form.role_id.data,
                    doc_type_id=form.doc_type_id.data
                )
    
                db.session.add(new_user)
                db.session.commit()
                db.session.close()
                return jsonify(f'{form.first_name.data} {form.last_name.data} Registrado exitosamente'), 201
            except Exception as e:
                return jsonify({'error': f'Ha ocurrido un error {e}'}), 500
        else:
                return jsonify({'errors': form.errors}),400

@require_content_type('aplications/JSON')
@user.route('/api/user/edit/<int:id>', methods=['GET','POST'])
def edit_user(id):

    with db.session.begin():
        user:object = User.query.get(id)
        db.session.close()

    if request.method == 'GET':
        return jsonify(user.to_dict())
    else:
        pass

@require_content_type('aplications/JSON')
@user.route('/api/user/delete/<int:id>',methods=['GET','POST'])
def delete_user(id):
    if request.method == 'GET':
        return jsonify(generate_token())
    else:
        try:
            user:object = User.query.get(id)
            if user:
                with db.session.begin():
                    db.session.delete(user)
                    db.session.commit()
                    db.session.close()
                return jsonify({f'Se ha eliminado el usuario'})
            else:
                return jsonify({f'No se ha encontrado el usuario'})
        except Exception as e:
            return jsonify({f'Ha ocurrido un error: {e}'})

@require_content_type('aplications/JSON')
@user.route('/api/user/list')
def get_users():
    try:
        with db.session.begin():
            users:list = User.query.all()
            db.session.close()
            return jsonify([user.to_dict() for user in users])
    except SQLAlchemyError as e:
        return jsonify({"error": "Error en la Base de Datos."}), 500
    except ValidationError as e:
        return jsonify({"error": "Error al procesar los datos"}), 400
    except Exception as e:
        return jsonify({"error": "Error inesperado"}), 500