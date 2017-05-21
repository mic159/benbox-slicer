
# def write_gcode(output_file, w, h, laser_values, resolution, speed):
#     output_file.write('; Created with benbox-slicer by mic159\n')
#     output_file.write('G28; home all axes\n')
#     output_file.write('G21; Set units to millimeters\n')
#     output_file.write('G90; Use absolute coordinates\n')
#
#     Laser_ON = False
#     current_power = None
#     for y in range(h):
#         last_pos = None
#         gcode_y = float(y)/resolution
#         row = range(w)
#         row_end = w - 1
#         # Alt rows are backwards
#         if y % 2:
#             row = reversed(range(w))
#             row_end = 0
#
#         for x in row:
#             gcode_x = float(x)/resolution
#
#             pixel = laser_values[y][x]
#             if pixel < 10:
#                 pixel = 0
#
#             if pixel > 0 and not Laser_ON:
#                 # Move while laser off
#                 output_file.write('G00 X{x} Y{y}\n'.format(x=gcode_x, y=gcode_y))
#             elif Laser_ON and pixel != current_power:
#                 # Move while laser on (use speed)
#                 output_file.write('G01 X{x} Y{y} F{speed}\n'.format(x=last_pos, y=gcode_y, speed=speed))
#
#             if not pixel and Laser_ON:
#                 output_file.write('M05; Laser OFF\n')
#                 current_power = pixel
#                 Laser_ON = False
#             elif pixel != current_power:
#                 output_file.write('M03; Laser on\n')
#                 current_power = pixel
#                 Laser_ON = True
#
#             last_pos = gcode_x
#
#         if Laser_ON:
#             # Hit the end of the row, and the laser is still on.
#             # Need to complete the row and turn off
#             gcode_x = float(row_end)/resolution
#             output_file.write('G01 X{x} Y{y} F{speed}\n'.format(x=gcode_x, y=gcode_y, speed=speed))
#             output_file.write('M05; Laser OFF\n')
#             current_power = 0
#             Laser_ON = False
#
#     # Finalise
#     output_file.write('G28; home all axes\n')


def gen_lines(input):
    current = None
    last_on = None
    for v, pos in input:
        if v >= 10 and current is None:
            current = pos
            last_on = pos
        elif v < 10 and current is not None:
            yield (current, last_on)
            current = None
            last_on = None
        elif v >= 10:
            last_on = pos
    if current is not None:
        yield (current, last_on)


def generate_range(output_file, w, h, start_x, start_y, laser_values, resolution, power):
    for y in range(start_y, start_y + h):
        gcode_y = float(y) / resolution
        row = laser_values[y][start_x:start_x + w]
        if y % 2:
            # Alt rows are backwards
            row = reversed(row)
        row = [
            (v, float(x + start_x) / resolution)
            for x, v in enumerate(row)
        ]

        for start, end in gen_lines(row):
            # Move while laser off
            output_file.write('G0 X{x} Y{y} S0\n'.format(x=start, y=gcode_y))
            output_file.write('G1 X{x} Y{y} S{power}\n'.format(x=end, y=gcode_y, power=power))


def write_gcode(output_file, w, h, laser_values, resolution, speed):
    output_file.write('; Created with benbox-slicer by mic159\n')
    output_file.write('G21; Set units to millimeters\n')
    output_file.write('G90; Use absolute coordinates\n')
    output_file.write('M3S0; Laser enabled\n')
    output_file.write('G1 F{speed}; Set speed\n'.format(speed=speed))
    for y in range(h, step=20):
        for x in range(w, step=20):
            generate_range(
                output_file,
                w=min(20, w - x), h=min(20, h - y),
                start_x=x,
                start_y=y,
                laser_values=laser_values,
                resolution=resolution,
                power=1000,  # TODO: proper value here
            )
    output_file.write('M5S0; Laser Off\n')
    output_file.write('M2; End\n')
