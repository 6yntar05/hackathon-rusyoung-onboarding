import os

middles = ["token"]
prefixes = ["", "."]
postfixes = ["", ".txt", ".json"]
case_sensivity = False

def possible_names() -> list:
    """
    Generate list of possible tokenfile names
    """
    _names = []

    for _middle in middles:
        for _prefix in prefixes:
            for _postfix in postfixes:
                _names.append(_prefix + _middle + _postfix)
    
    return _names

def token_validate(text:str) -> bool:
    """
    Validate token. Considers lenght only for now
    """
    if len(text) != 46:
        return False
    return True

def token_get() -> str:
    """
    Read the token from file (check `possible_names()`)
    """
    _names = possible_names()
    ls = os.listdir()
    for filename in ls:
        if filename in _names:
            _file = open(filename, "r")
            _text = _file.read()
            _token = _text.replace("\n", "").replace("{", "").replace("}", "").replace(" ", "")
            if not token_validate(_token):
                raise ValueError("Uncorrect token!")
            return _token
    
    raise NameError("Unnable to find tokenfile. Write the token in ..token.txt file, for example")