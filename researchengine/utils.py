import  json

def to_obj(s):
    """
    Converts JSON text from the LLM into a Python object.
    """
    try:
        return json.loads(s)
    except Exception:
        return {}