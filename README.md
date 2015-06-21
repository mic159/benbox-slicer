Benbox PNG Slicer
=================

Converts PNG raster images into Gcode to be sent to the Benbox Laser Engraver.

Also includes an [OctoPrint](http://octoprint.org/) plugin!

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

OctoPrint plugin
================

This also includes a plugin for [OctoPrint](http://octoprint.org/).

To install it, all you have to do is pip install this along with octoprint!

```
pip install octoprint
pip install benbox-slicer
```

Setting up the benbox with OctoPrint
----------

Currently the benbox does not work out of the box with OctoPrint :(

The benbox does not support checksums in GCODE, and you will have to modify the source code to
make it work.

Open up [octoprint/util/comm.py](https://github.com/foosel/OctoPrint/blob/e722c2f8adef5dce085205977a0e83331aba5837/src/octoprint/util/comm.py#L1524)
to around line 1524 and comment out or delete the code so that it always just uses `_doSendWithoutChecksum`.

For example:
```python
# now comes the part where we increase line numbers and send stuff - no turning back now
#if (gcode is not None or self._sendChecksumWithUnknownCommands) and (self.isPrinting() or self._alwaysSendChecksum):
#    linenumber = self._currentLine
#    self._addToLastLines(command)
#    self._currentLine += 1
#    self._doSendWithChecksum(command, linenumber)
#else:
self._doSendWithoutChecksum(command)
```
