#basic json serializer class found here:
#https://stackoverflow.com/questions/6908107/serializing-and-deserializing-object-with-json

import JSON

class Serializer:
    @staticmethod
    def encode_obj(obj):
        if type(obj).__name__ =='instance':
            return obj.__dict__

    @staticmethod
    def serialize(obj):
        return json.dumps(obj, default=Serializer.encode_obj)
