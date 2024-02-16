from flask import request, jsonify
from http import HTTPStatus
from . import app
from .services import update_user_balance, get_user_by_id, create_user, delete_user
from .weather_service import fetch_weather

def validate_balance(balance):
    """Проверка корректности баланса."""
    if balance > 15000 or balance < 5000:
        return False
    return True

@app.route('/create-user', methods=['POST'])
def create_user_route():
    data = request.get_json()
    username, balance = data.get('username'), data.get('balance')

    if not username or balance is None:
        return jsonify({"error": "Missing username or balance"}), HTTPStatus.BAD_REQUEST

    if not validate_balance(balance):
        return jsonify({"error": "The balance should be between 5000-15000"}), HTTPStatus.BAD_REQUEST

    user = create_user(username, balance)
    return jsonify({"message": "User created successfully", "userId": user.id, "username": user.username, "balance": user.balance}), HTTPStatus.CREATED

@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    if not get_user_by_id(user_id):
        return jsonify({"error": "User not found"}), HTTPStatus.NOT_FOUND

    if delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), HTTPStatus.OK
    return jsonify({"error": "Failed to delete user"}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/update-balance', methods=['POST'])
def update_balance():
    user_id, city = request.json.get('userId'), request.json.get('city')

    if not user_id or not city:
        return jsonify({"error": "Missing userId or city"}), HTTPStatus.BAD_REQUEST

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), HTTPStatus.NOT_FOUND

    try:
        temperature = fetch_weather(city)
        if user.balance - abs(temperature) < 0:
            return jsonify({"error": "The balance is lower than 0"}), HTTPStatus.BAD_REQUEST

        updated_user = update_user_balance(user_id, temperature)
        if updated_user:
            return jsonify({"message": "Balance updated successfully", "userId": updated_user.id, "newBalance": updated_user.balance}), HTTPStatus.OK
    except Exception as e:
        print(e)

    return jsonify({"error": "Failed to update balance"}), HTTPStatus.BAD_REQUEST
