import uuid

def generate_id(prefix=""):

    id =  str(uuid.uuid4()).replace("-","")[:8]
    return f"{prefix}{id}"
    