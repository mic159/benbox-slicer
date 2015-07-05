

def write_gcode(output_file, w, h, laser_values, resolution, speed):
    output_file.write('; Created with benbox-slicer by mic159\n')
    output_file.write('G28; home all axes\n')
    output_file.write('G21; Set units to millimeters\n')
    output_file.write('G90; Use absolute coordinates\n')
    output_file.write('G92; Coordinate Offset\n')

    Laser_ON = False
    current_power = None
    for y in range(h):
        gcode_y = float(y)/resolution
        row = range(w)
        row_end = w
        # Alt rows are backwards
        if y % 2:
            row = reversed(range(w))
            row_end = 0

        for x in row:
            gcode_x = float(x)/resolution

            pixel = laser_values[y][x]
            if pixel < 10:
                pixel = 0

            if pixel > 0 and not Laser_ON:
                # Move while laser off
                output_file.write('G00 X{x} Y{y}\n'.format(x=gcode_x, y=gcode_y))
            elif Laser_ON and pixel != current_power:
                # Move while laser on (use speed)
                output_file.write('G01 X{x} Y{y} F{speed}\n'.format(x=gcode_x, y=gcode_y, speed=speed))


            if not pixel and Laser_ON:
                output_file.write('M05; Laser OFF\n')
                current_power = pixel
                Laser_ON = False
            elif pixel != current_power:
                output_file.write('M03 L{intensity}; Laser power\n'.format(intensity=pixel))
                current_power = pixel
                Laser_ON = True

        if Laser_ON:
            # Hit the end of the row, and the laser is still on.
            # Need to complete the row and turn off
            gcode_x = float(row_end)/resolution
            output_file.write('G01 X{x} Y{y} F{speed}\n'.format(x=gcode_x, y=gcode_y, speed=speed))
            output_file.write('M05; Laser OFF\n')
            current_power = 0
            Laser_ON = False


    # Finalise
    output_file.write('G28; home all axes\n')