from middlewares.auth_middleware import token_required
from flask import Blueprint, request, jsonify
from models.user import User
from models.planner import Planner



auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/create-or-update-user", methods=["POST"])
@token_required
def create_or_update_user():
    """Create a new user if they don't exist, else update existing user details."""
    data = request.json
    uid = data.get("uid")
    email = data.get("email")
    name = data.get("name")
    roll_number = data.get("roll_number")
    branch = data.get("branch")
    year = data.get("year")
    semester = data.get("semester")
    subjects = data.get("subjects", [])
    attendance_period = {
    "start": data.get("startDate"),
    "end": "2026-05-31"
  }
    profileCompleted = data.get("profileCompleted")

    if not uid or not email:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    existing_user = User.get_user_by_id(uid)

    if existing_user:
        # Update existing user
        updated_data = {
            "name": name or existing_user.get("name"),
            "roll_number": roll_number or existing_user.get("roll_number"),
            "branch": branch or existing_user.get("branch"),
            "year": year or existing_user.get("year"),
            "semester": semester or existing_user.get("semester"),
            "subjects": subjects or existing_user.get("subjects"),
            "attendance_period": attendance_period or existing_user.get("attendance_period"),
            "profileCompleted":profileCompleted
        }
        result = User.edit_user(uid, updated_data)
        planner_data = Planner.generate_planner(uid)  # Assuming this function generates the planner
        if "error" in planner_data:
            return jsonify(planner_data), 400

        return jsonify({"message": "User updated successfully", "uid": uid, "planner": planner_data})

    # Create new user
    new_user = User.create_user(uid, email, name, roll_number, branch, year, semester, subjects, attendance_period)
    planner_data = Planner.generate_planner(uid)  # Assuming this function generates the planner
    if "error" in planner_data:
        return jsonify(planner_data), 400

    return jsonify({"message": "User created successfully", "user": new_user})
