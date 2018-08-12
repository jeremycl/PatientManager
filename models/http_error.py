import json

class HttpError:

    def __init__(self, id: str=None, status: str=None, title: str=None, detail: str=None, code: str=None, source: object=None):
        self.id = id
        self.status = status
        self.title = title
        self.detail = detail
        self.code = code
        self.source = source

    @property
    def serialize(self):
        sourceObj = {}

        if isinstance(self.source, dict):
            sourceObj = self.source

        elif type(self.source) is Exception:
            if (self.source.__class__) and (self.source.args.__len__() > 0):
                sourceObj = {
                    'type': self.source.__class__.__name__,
                    'arg': self.source.args[0]
                }
            else:
                sourceObj = {}

        return {
                'code': self.code,
                'detail': self.detail,
                'id': self.id,
                'source': sourceObj,
                'status': self.status,
                'title': self.title
        }
