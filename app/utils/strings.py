import re

pattern = re.compile(r'(?<!^)(?=[A-Z])')


def snakecase(string: str) -> str:
    """Convert string into snake case.
    Join punctuation with underscore
    Args:
        string: String to convert.
    Returns:
        string: Snake cased string.
    """
    return pattern.sub('_', string).lower()


def to_str(x, charset='utf8', errors='strict'):
    if x is None or isinstance(x, str):
        return x

    if isinstance(x, bytes):
        return x.decode(charset, errors)

    return str(x)
