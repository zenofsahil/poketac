def remove_nonprintable_chars(string: str) -> str:
    """ 
    Replace non-printable characters from the given `string` with space.
    """
    return "".join([s if s.isprintable() else ' ' for s in string])





