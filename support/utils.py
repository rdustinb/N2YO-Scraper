import uuid

def genRandomId():
    # See RFC4122 for more information as this package generates random UUIDs based on that specification:
    # https://www.rfc-editor.org/rfc/rfc4122
    #
    # The function uuid1, uuid3, uuid4, and uuid5 provide the different versions of UUIDs
    return str(uuid.uuid4())
