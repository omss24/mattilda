import threading

_lock = threading.Lock()
_requests_total = 0


def increment_requests() -> None:
    global _requests_total
    with _lock:
        _requests_total += 1


def get_requests_total() -> int:
    with _lock:
        return _requests_total
