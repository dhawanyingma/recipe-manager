import logging
import time
import uuid
from flask import request, g


class LogUtil:

    @staticmethod
    def init_app(app):

        #configure base logging format
        logging.basicConfig(
            level=logging.INFO, 
            format="%(asctime)s - [%(levelname)s] - %(message)s"
        )

        @app.before_request
        def start_timer():
            g.start_time = time.time()
            g.request_id = str(uuid.uuid4())   

        @app.after_request
        def log_request(response):
            duration = round((time.time() - g.start_time) * 1000, 2)
            log_entry = {
                "request_id" : g.request_id,
                "method" : request.method,
                "path" : request.path,
                "status" : response.status_code,
                "duration_ms" : duration
            }
            app.logger.info(log_entry)
            response.headers["X-Request-ID"] = g.request_id
            return response
