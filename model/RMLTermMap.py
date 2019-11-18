from enum import Enum


class TermMapType(Enum):
    CONSTANT_MAP = 1
    COLUMN_MAP = 2
    TEMPLATE_MAP = 3


class RMLTermMap:
    def __init__(self, term_map_type, term_map_value):
        self.term_map_type = term_map_type
        self.term_map_value = term_map_value


def string_separetion(string):
    if ("{" in string) :
        prefix = string.split("{")[0]
        condition = string.split("{")[1].split("}")[0]
        postfix = string.split("{")[1].split("}")[1]
        field = prefix + "*" + postfix
    elif "[" in string:
        return string, string
    else:
        return string, ""
    return string, condition