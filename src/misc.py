import random


def random_color_int():
    """Gets random color integer

    Returns:
        int: color
    """
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    color = 65536*r + 256*g + b
    return color