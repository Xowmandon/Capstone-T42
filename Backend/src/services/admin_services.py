# Author: Joshua Ferguson

from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import Backend.src.models as models  # Assuming a User model with an "is_admin" field

# Decorator to protect routes that require admin access
def admin_protected(f):
    @wraps(f)
    @jwt_required()  # Ensures user is authenticated before checking admin status
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()  # Fetch user ID from the token
        user = models.User.query.get(user_id)

        if not user or not user.is_admin:
            return jsonify({"message": "Admin access required"}), 403

        return f(*args, **kwargs)

    return decorated_function

# Decorator to protect services that require admin access, but don't use JWT or Requests
def admin_protected_service(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_id = kwargs.get("admin_id")  # Fetch user ID from the request parameters
        admin = models.User.query.get(admin_id)

        if not admin or not admin.is_admin:
            return jsonify({"message": "Admin access required"}), 403

        return f(*args, **kwargs)

    return decorated_function

class AdminDashboardService:
    @admin_protected_service
    def get_dashboard_data(self, admin_id):
        return {
            "total_users": models.User.query.count(),
            "total_messages": models.Message.query.count(),
            "total_matches": models.Match.query.count(),
            "total_reports": models.Report.query.count()
        }
        
    @admin_protected_service
    def get_admins(self, admin_id):
        return models.User.query.filter_by(is_admin=True).all()
    
class AdminService:
    @admin_protected
    def promote_to_admin(self,admin_id,user_id):
        user = models.User.query.get(user_id)
        if user:
            user.is_admin = True
            models.db.session.commit()
            return jsonify({"message": "User promoted to admin"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    @admin_protected
    def demote_from_admin(self, admin_id, user_id):
        user = models.User.query.get(user_id)
        if user:
            user.is_admin = False
            models.db.session.commit()
            return jsonify({"message": "User demoted from admin"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
        