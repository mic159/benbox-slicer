from benbox_slicer import png

"""
Convert the PNG data to a flat array of greyscale pixels (0-255)
"""


def read_image(input_file, conv_method=None):
    '''
    Open the PNG file and convert it to greyscale values.

    Supports multiple conversion methods. See below for built-ins.

    :param input_file:  Open file object for reading
    :param conv_method: The conversion lambda. Takes in 3 args: r, g, b. See below for samples.
    :return:  tuple (w, h, image_data). The image_data is a 2d array of greyscale values (0-255).
    '''
    if conv_method == None:
        conv_method = mix
    reader = png.Reader(input_file)

    w, h, pixels, metadata = reader.read_flat()
    result = []
    for y in range(h):
        row = []
        for x in range(w):
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            r,g,b = pixels[pixel_position:pixel_position+3]
            value = conv_method(r, g, b)
            row.append(int(value))
        result.append(row)
    return w, h, result


# Here are the options to pick from. Default is 'mix'.
mix = lambda r, g, b: r * 0.21 + g * 0.71 + b * 0.07  # 0.21R + 0.71G + 0.07B
average = lambda r, g, b: (r + g + b) / 3             # (R+G+B)/3
red = lambda r, g, b: r                               # Use the red channel only
green = lambda r, g, b: g                             # Use the green channel only
blue = lambda r, g, b: b                              # Use the blue channel only
max_color = lambda r, g, b: max(r, g, b)              # Use the maximum value from all colors
min_color = lambda r, g, b: min(r, g, b)              # Use the minimum of all colors
