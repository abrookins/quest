import threading

request_config = threading.local()


class RouterMiddleware(object):
    def process_view(self, request, view_func, args, kwargs):
        if request.is_authenticated():
            request_config.user_id = request.user.id

    def process_response(self, request, response):
        if hasattr(request_config, 'user_id'):
            del request_config.user_id
        return response
