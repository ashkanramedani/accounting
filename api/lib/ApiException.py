import http


class API_Exception(Exception):
    Known_Error = [
        'psycopg2.errors.UniqueViolation'
    ]

    def __init__(self, status_code: int, detail: Exception | None = None) -> None:
        self.detail = http.HTTPStatus(status_code).phrase if detail is None else detail.args
        for exception in self.Known_Error:
            if exception in detail.__repr__():
                self.detail = exception
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"
