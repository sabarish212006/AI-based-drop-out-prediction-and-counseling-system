"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: error_handlers.py
Purpose: Global Error Handlers
----------------------------------------------------------
"""

from flask import jsonify, render_template


def register_error_handlers(app):
    """
    Register all global error handlers.
    """

    # ==========================================
    # 404 - Page Not Found
    # ==========================================
    @app.errorhandler(404)
    def page_not_found(error):
        """
        Handle 404 errors.
        """

        if app.config.get("DEBUG"):
            return jsonify({
                "success": False,
                "error": "Page not found (404)"
            }), 404

        return render_template("errors/404.html"), 404

    # ==========================================
    # 500 - Internal Server Error
    # ==========================================
    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Handle 500 errors.
        """

        if app.config.get("DEBUG"):
            return jsonify({
                "success": False,
                "error": "Internal server error (500)"
            }), 500

        return render_template("errors/500.html"), 500

    # ==========================================
    # 400 - Bad Request
    # ==========================================
    @app.errorhandler(400)
    def bad_request(error):
        """
        Handle 400 errors.
        """

        if app.config.get("DEBUG"):
            return jsonify({
                "success": False,
                "error": "Bad request (400)"
            }), 400

        return render_template("errors/400.html"), 400

    # ==========================================
    # 403 - Forbidden
    # ==========================================
    @app.errorhandler(403)
    def forbidden(error):
        """
        Handle 403 errors.
        """

        if app.config.get("DEBUG"):
            return jsonify({
                "success": False,
                "error": "Forbidden (403)"
            }), 403

        return render_template("errors/403.html"), 403