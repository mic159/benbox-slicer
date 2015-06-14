import png
import benbox_slicer.image_reader
import benbox_slicer.conversion


def do_slice(input_file, speed, mode='bw', resolution=10, flip_y=False):
    reader = png.Reader(input_file)

    w, h, pixels, metadata = reader.read_flat()

    greyscale_image = benbox_slicer.image_reader.mix(w, h, pixels, metadata)
    del pixels
    del metadata

    if mode == 'bw':
        laser_values = benbox_slicer.conversion.on_off(greyscale_image, w, h, threshold=128)
    elif mode == 'random':
        laser_values = benbox_slicer.conversion.random_threshold(greyscale_image, w, h)
    elif mode == 'greyscale':
        laser_values = benbox_slicer.conversion.greyscale(greyscale_image, w, h, resolution=128)
    else:
        raise ValueError('Mode not supported')
    del greyscale_image

    # Write preview PNG
    with open('preview.png', 'wb') as fle:
        img = png.Writer(w, h, greyscale=True, bitdepth=8)
        img.write(fle, laser_values)


    if not flip_y:
        # 0,0 is normally at the bottom left so we flip the data
        laser_values.reverse()


    Laser_ON = False

    with open('output.gcode', 'w') as file_gcode:
        file_gcode.write('; Created with benbox-slicer by mic159\n')
        file_gcode.write('G28; home all axes\n')
        file_gcode.write('G21; Set units to millimeters\n')
        file_gcode.write('G90; Use absolute coordinates\n')
        file_gcode.write('G92; Coordinate Offset\n')

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
                    file_gcode.write('G00 X{x} Y{y}\n'.format(x=gcode_x, y=gcode_y))
                elif Laser_ON and pixel != current_power:
                    # Move while laser on (use speed)
                    file_gcode.write('G01 X{x} Y{y} F{speed}\n'.format(x=gcode_x, y=gcode_y, speed=speed))


                if not pixel and Laser_ON:
                    file_gcode.write('M05; Laser OFF\n')
                    current_power = pixel
                    Laser_ON = False
                elif pixel != current_power:
                    file_gcode.write('M03 L{intensity}; Laser power\n'.format(intensity=pixel))
                    current_power = pixel
                    Laser_ON = True

            if Laser_ON:
                # Hit the end of the row, and the laser is still on.
                # Need to complete the row and turn off
                gcode_x = float(row_end)/resolution
                file_gcode.write('G01 X{x} Y{y} F{speed}\n'.format(x=gcode_x, y=gcode_y, speed=speed))
                file_gcode.write('M05; Laser OFF\n')
                current_power = 0
                Laser_ON = False


        # Finalise
        file_gcode.write('G00 X0 Y0; home\n')
        file_gcode.write('G28; home all axes\n')