from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error" :{
                "code" : "NOT FOUND",
                "message" : "The requested resource was not found"
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "error" : {
                "code" : "INTERNAL_SERVER_ERROR",
                "message" : "An unexpected error occured"
            }
        }), 500
    
    