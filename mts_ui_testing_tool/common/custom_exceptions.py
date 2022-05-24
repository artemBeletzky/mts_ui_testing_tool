class TabNotFound(Exception):
    def __init__(self, data_test_id):
        message = f"Не удалось найти таб с data-test-id '{data_test_id}'"
        super().__init__(message)

# class TabNotFoundWithin