class Pagination:
    def __init__(self, _self: str=None, _next: str=None):
        self.self = _self
        self.next = _next

    @property
    def serialize(self):
        return {
            'self': self.self,
            'next': self.next
        }