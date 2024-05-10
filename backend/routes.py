from flask import request, jsonify, make_response
from app import db, app
from models import User


@app.route("/test", methods=["GET"])
def test_route():
    return make_response(jsonify({"message": "The server is running"}), 200)


@app.route("/api/flask/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name=data["name"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        new_data = {"id": new_user.id, "name": new_user.name, "email": new_user.email}
        return make_response(jsonify(new_data), 201)
    except Exception as e:  # pylint: disable=broad-except
        return make_response(
            jsonify({"message": "error creating user", "error": str(e)}), 500
        )


@app.route("/api/flask/users", methods=["GET"])
def get_all_users():
    try:
        users = User.query.all()
        users_data = [
            {"id": user.id, "name": user.name, "email": user.email} for user in users
        ]
        return make_response(jsonify(users_data), 200)
    except Exception as e:  # pylint: disable=broad-except
        return make_response(
            jsonify({"message": "error getting users", "error": str(e)}), 500
        )


@app.route("/api/flask/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            return make_response(jsonify(user.json()), 200)
        return make_response(jsonify({"message": f"user {user_id} not found"}), 404)
    except Exception as e:  # pylint: disable=broad-except
        return make_response(
            jsonify({"message": f"error getting user {user_id}", "error": str(e)}), 500
        )


@app.route("/api/flask/users/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            data = request.get_json()
            user.name = data["name"]
            user.email = data["email"]
            db.session.commit()
            return make_response(jsonify({"message": f"user {user_id} updated"}), 200)
        return make_response(jsonify({"message": f"user {user_id} not found"}), 404)
    except Exception as e:  # pylint: disable=broad-except
        return make_response(
            jsonify({"message": f"error updating user {user_id}", "error": str(e)}), 500
        )


@app.route("/api/flask/users/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": f"user {user_id} deleted"}), 200)
        return make_response(jsonify({"message": f"user {user_id} not found"}), 404)
    except Exception as e:  # pylint: disable=broad-except
        return make_response(
            jsonify({"message": f"error deleting user {user_id}", "error": str(e)}), 500
        )


db.create_all()
if __name__ == "__main__":
    app.run(debug=True)
