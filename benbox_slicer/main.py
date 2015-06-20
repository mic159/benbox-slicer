import argparse
from benbox_slicer.slicer import do_slice


class ChoicesInput(object):
    def __init__(self, choices, cast):
        self.choices = choices
        self.cast = cast

    def __call__(self, input):
        try:
            input = self.cast(input)
        except ValueError:
            pass
        if input not in self.choices:
            raise argparse.ArgumentTypeError('Choices are '+ str(self.choices))
        return input

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=argparse.FileType('r'), help='File to slice', required=True)
    parser.add_argument('--speed', type=int, default=200, help='The speed of the laser while on')
    parser.add_argument('--resolution',
                        type=ChoicesInput([1,2,5,10], cast=int),
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
