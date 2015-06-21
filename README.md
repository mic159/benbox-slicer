Benbox PNG Slicer
=================

Converts PNG raster images into Gcode to be sent to the Benbox Laser Engraver.

Usage
-----

Basic usage looks like this:
```
benbox-slicer --input test.png
```

The results will be in a file called `output.gcode` in the current directory.

Other options:

 - `--speed` The speed to make the laser go while its on. Defaults to 200.
 - `--resolution` Lines per mm. 10 works best with the benbox. Defaults to 10.
 - `--mode` Mode of converting from the PNG to the laser. See below. Defaults to `bw`.

Mode
----

### bw

B/W mode uses a simple threashold if brightness to determine if the pixel should be burnt or not.

![BW mode preview](examples/preview-bw.png?raw=true)

### random

Random tries to use little dots to emulate greys.

![Random mode preview](examples/preview-random.png?raw=true)

### greyscale

This mode attempts to use the laser's intensity to draw different tones of grey.

It is experimental, and doesnt seem to work all that well for me yet, but why not give it a go?

![Greyscale mode preview](examples/preview-greyscale.png?raw=true)

