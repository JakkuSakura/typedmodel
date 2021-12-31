

class TypeException(Exception):
    def __init__(self, reason):
        self.args = (reason,)


class ExtraArgumentException(Exception):
    def __init__(self, reason):
        self.args = (reason,)


class MissingArgumentException(Exception):
    def __init__(self, reason):
        self.args = (reason,)
