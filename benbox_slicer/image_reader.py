from benbox_slicer import png

"""
Convert the PNG data to a flat array of greyscale pixels (0-255)
"""

def read_image(input_file, conv_method=None):
    if conv_method == None:
        conv_method = mix
    reader = png.Reader(input_file)

    w, h, pixels, metadata = reader.read_flat()
    return w, h, conv_method(w, h, pixels, metadata)

def mix(w, h, pixels, metadata):
    #0.21R + 0.71G + 0.07B
    result = []
    for y in range(h):
        row = []
        for x in range(w):
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            r,g,b = pixels[pixel_position:pixel_position+3]
            value = r * 0.21 + g * 0.71 + b * 0.07
            row.append(int(value))
        result.append(row)
    return result

def average(w, h, pixels, metadata):
    # (R+G+B)/3
    for y in range(h): # y varia da 0 a h-1
        for x in range(w): # x varia da 0 a w-1
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            matrice[y][x] = int((pixels[pixel_position] + pixels[(pixel_position+1)]+ pixels[(pixel_position+2)]) / 3 )

def red(w, h, pixels, metadata):
    # Use the red channel only
    for y in range(h): # y varia da 0 a h-1
        for x in range(w): # x varia da 0 a w-1
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            matrice[y][x] = int(pixels[pixel_position])

def green(w, h, pixels, metadata):
    # Use the green channel only
    for y in range(h): # y varia da 0 a h-1
        for x in range(w): # x varia da 0 a w-1
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            matrice[y][x] = int(pixels[(pixel_position+1)])

def blue(w, h, pixels, metadata):
    # Use the blue channel only
    for y in range(h): # y varia da 0 a h-1
        for x in range(w): # x varia da 0 a w-1
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            matrice[y][x] = int(pixels[(pixel_position+2)])

def max_color(w, h, pixels, metadata):
    # Use the maximum value from all colors
    for y in range(h): # y varia da 0 a h-1
        for x in range(w): # x varia da 0 a w-1
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            list_RGB = pixels[pixel_position] , pixels[(pixel_position+1)] , pixels[(pixel_position+2)]
            matrice[y][x] = int(max(list_RGB))

def min_color(w, h, pixels, metadata):
    # Use the minimum of all colors
    for y in range(h): # y varia da 0 a h-1
        for x in range(w): # x varia da 0 a w-1
            pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
            list_RGB = pixels[pixel_position] , pixels[(pixel_position+1)] , pixels[(pixel_position+2)]
            matrice[y][x] = int(min(list_RGB))