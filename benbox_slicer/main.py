import argparse
import benbox_slicer.image_reader
import benbox_slicer.conversion
import benbox_slicer.gcode
from benbox_slicer import png


class ChoicesInput(object):
    def __init__(self, choices, cast):
        self.choices = choices
        self.cast = cast

    def __call__(self, value):
        try:
            value = self.cast(value)
        except ValueError:
            pass
        if value not in self.choices:
            raise argparse.ArgumentTypeError('Choices are ' + str(self.choices))
        return value


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=argparse.FileType('r'), help='File to slice', required=True)
    parser.add_argument('--speed', type=int, default=200, help='The speed of the laser while on')
    parser.add_argument('--resolution',
                        type=ChoicesInput([1, 2, 5, 10], cast=int),
                        default=10,
                        help='The resolution in lines per mm. Choices: 1, 2, 5, 10'
                        )
    parser.add_argument('--mode',
                        type=ChoicesInput(['bw', 'random', 'greyscale'], cast=str),
                        default='bw',
                        help='The slicing mode. Choices: bw, random, greyscale'
                        )

    args = parser.parse_args()

    do_slice(args.input, speed=args.speed, resolution=args.resolution, mode=args.mode)


def do_slice(input_file, speed, mode='bw', resolution=10, flip_y=False):
    w, h, image = benbox_slicer.image_reader.read_image(input_file)

    if mode == 'bw':
        laser_values = benbox_slicer.conversion.on_off(image, w, h, threshold=128)
    elif mode == 'random':
        laser_values = benbox_slicer.conversion.random_threshold(image, w, h)
    elif mode == 'greyscale':
        laser_values = benbox_slicer.conversion.greyscale(image, w, h, resolution=128)
    else:
        raise ValueError('Mode not supported')
    del image

    # Write preview PNG
    with open('preview.png', 'wb') as fle:
        img = png.Writer(w, h, greyscale=True, bitdepth=8)
        img.write(fle, laser_values)

    if not flip_y:
        # 0,0 is normally at the bottom left so we flip the data
        laser_values.reverse()

    with open('output.gcode', 'w') as file_gcode:
         benbox_slicer.gcode.write_gcode(file_gcode, w, h, laser_values, resolution=resolution, speed=speed)
