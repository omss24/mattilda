requests_total = 0


def increment_requests() -> None:
    global requests_total
    requests_total += 1


def get_requests_total() -> int:
    return requests_total
