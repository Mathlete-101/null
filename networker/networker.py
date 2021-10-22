requests = {}


def request(obj, request_type):
    if request_type not in requests:
        requests[request_type] = []
    requests[request_type].push(obj)
    update_requests()


def update_requests():
    pass


def generate():
    pass
