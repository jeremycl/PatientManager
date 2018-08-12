class MultipleErrors(Exception):
    def __init__(self, errors):
        self.errors = errors

class InputError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    @property
    def serialize(self):
        return {
            'expression': self.expression,
            'message': self.message
        }

class DuplicateError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    @property
    def serialize(self):
        return {
            'expression': self.expression,
            'message': self.message
        }