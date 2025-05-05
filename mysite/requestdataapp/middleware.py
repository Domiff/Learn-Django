# from django.http import HttpRequest
#
#
# def set_useragent_on_request_middleware(get_response):
#
#     print("Initial call")
#
#     def middleware(request: HttpRequest):
#         print("before get response")
#         request.user_agent = request.META["HTTP_USER_AGENT"]
#         response = get_response(request)
#         print("after get response")
#
#         return response
#
#     return middleware
#
#
# class CountRequestMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.request_count = 0
#         self.response_count = 0
#         self.exception_count = 0
#
#     def __call__(self, request: HttpRequest):
#         self.request_count += 1
#         print("Count request: ", self.request_count)
#
#         response = self.get_response(request)
#
#         self.response_count += 1
#         print("Count response: ", self.response_count)
#
#         return response
#
#     def process_exception(self, request: HttpRequest, exec: Exception):
#         self.exception_count += 1
#         print("Count exception: ", self.exception_count)
