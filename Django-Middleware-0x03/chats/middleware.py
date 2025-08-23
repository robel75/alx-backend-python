from django.conf import settings
from django.core.exceptions import PermissionDenied
from datetime import datetime
import logging
from collections import deque

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        with open("requests.log", "a")as f:
            f.write(f"{datetime.now()} - user : {user}, -path: {request.path}\n")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response= get_response

    def __call__(self, request):
        if (18,0)<datetime.now().time()<(21,0):
            raise PermissionDenied


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = {}
        self.time_window=60
        self.times_requested=5
    
    def __call__(self, request):
        client_ip = self.get.client_ip(request)
        now = time.time()

        if client_ip not in request_log:
            self.request_log[client_ip]=deque()

        request_times = self.request_log[client_ip]
       