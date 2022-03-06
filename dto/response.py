class BaseResponse:
    def __init__(self, code=200, des="service is running", res="ok"):
        self.code = code
        self.description = des
        self.result = res
