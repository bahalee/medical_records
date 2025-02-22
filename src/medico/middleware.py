class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request path: {request.path}")  # Debug print
        print(f"User authenticated: {request.user.is_authenticated}")  # Debug print
        response = self.get_response(request)
        return response