import time
import json
from django.utils.deprecation import MiddlewareMixin

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        log_data = {
            "method": request.method,
            "path": request.get_full_path(),
            "status_code": response.status_code,
            "duration": f"{duration:.3f}s",
        }
        # Write logs to file instead of console
        with open("request_logs.txt", "a") as log_file:
            log_file.write(json.dumps(log_data) + "\n")
        return response
