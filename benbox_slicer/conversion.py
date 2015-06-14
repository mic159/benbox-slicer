from random import randint


def on_off(image, w, h, threshold=128):
    """
    Black and white (no greyscale) with a simple threshold.
    If the color is dark enough, the laser is on!
    """
    result = []

    for row in image:
        result_row = []
        for pixel in row:
            # We draw black, so 255 is for dark pixels
            result_row.append(255 if pixel < threshold else 0)
        result.append(result_row)
    return result


def random_threshold(image, w, h):
    """
    Black and white (no greyscale) with random dots.
    Attempts to show tones by putting random dots in.
    """
    result = []
    for row in image:
        result_row = []
        for pixel in row:
            threshold = randint(20,235)
            result_row.append(255 if pixel < threshold else 0)
        result.append(result_row)
    return result


def greyscale(image, w, h, resolution=256):
    """
    Uses the laser's power to show greys.
    The resolution is how much power to vary by on the high end.

    eg. 16 will give laser power 255 to 238
    """
    offset = 255 - resolution - 1
    result = []
    for row in image:
        result_row = []
        for pixel in row:
            if pixel <= 5:
                # 0 is black, so full laser power
                result_row.append(255)
            elif pixel >= 240:
                # 255 is white, so no laser
                result_row.append(0)
            else:
                # Note inverting
                percentage = (1 - (pixel / 255.0))
                result_row.append(offset + int(percentage * (resolution - 1)))
        result.append(result_row)
    return result
