def find_lowest_under(len_text: int = 0, text: str = "", max: int = 1500):
    """[summary]

    Args:
        len_text (int, optional): [length of the text]. Defaults to 0.
        text (str, optional): [the text itself]. Defaults to "".

    Returns:
        [int]: [returns the lowest amount of divisions when the text is under n chars]
    """
    if not len_text:
        len_text = len(text)
    i = 1
    while not len_text / i < max:
        i += 1

    return i  