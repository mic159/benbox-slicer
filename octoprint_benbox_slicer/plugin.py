import json
import octoprint.plugin
import octoprint.slicing
import octoprint.filemanager

import benbox_slicer.image_reader
import benbox_slicer.conversion
import benbox_slicer.gcode


def png_file_support(*args, **kwargs):
    return {
        'model': {
            'png': ['png']
        }
    }


class BenboxSlicer(octoprint.plugin.SlicerPlugin,
                   octoprint.plugin.StartupPlugin):
    TYPE = 'benboxslicer'

    def on_startup(self, host, port):
        from octoprint.server import slicingManager
        try:
            slicingManager.get_profile_path(self.TYPE, 'speed_20', must_exist=True)
        except octoprint.slicing.exceptions.UnknownProfile:
            self._logger.info('No default profiles, creating...')
            profile = self.make_profile(speed=20)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )
            profile = self.make_profile(speed=30)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )
            profile = self.make_profile(speed=40)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )
            profile = self.make_profile(speed=50)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )
            profile = self.make_profile(speed=80)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )
            profile = self.make_profile(speed=100)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )
            profile = self.make_profile(speed=120)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )
            profile = self.make_profile(speed=200)
            self.save_slicer_profile(
                path=slicingManager.get_profile_path(self.TYPE, profile.name),
                profile=profile,
            )

    def is_slicer_configured(self):
        return True

    def get_slicer_properties(self):
        return dict(
            type=self.TYPE,
            name='Benbox PNG',
            same_device=True,
            progress_report=False,
            source_file_types=['png'],
        )

    def save_slicer_profile(self, path, profile, allow_overwrite=True, overrides=None):
        data = profile.data
        if overrides:
            data.update(overrides)
        data['display_name'] = profile.display_name
        data['description'] = profile.description
        data['name'] = profile.name
        with open(path, 'w') as fle:
            json.dump(data, fle)

    def get_slicer_profile(self, path):
        with open(path, 'r') as fle:
            data = json.load(fle)
        profile = octoprint.slicing.SlicingProfile(
            self.TYPE,
            name=data.get('name', 'unknown'),
            data=data,
            display_name=data.get('display_name', 'Unknown'),
            description=data.get('description', '')
        )
        return profile

    def make_profile(self, speed=20):
        default_settings = {
            'speed': speed,
            'mode': 'bw',
            'resolution': 10
        }
        profile = octoprint.slicing.SlicingProfile(
            self.TYPE,
            name='speed_{speed}'.format(**default_settings),
            data=default_settings,
            display_name='Speed: {speed}'.format(**default_settings),
            description='Speed: {speed}, Resolution: {resolution}, Mode: {mode}.'.format(**default_settings)
        )
        return profile

    def get_slicer_default_profile(self):
        return self.make_profile(speed=20)

    def do_slice(self, model_path, printer_profile, machinecode_path=None,
                 profile_path=None, position=None,
                 on_progress=None, on_progress_args=None, on_progress_kwargs=None
                 ):
        if not machinecode_path:
            machinecode_path = model_path + '.gcode'
        self._logger.info('Slicing to %s', machinecode_path)

        profile = self.get_slicer_profile(profile_path)
        self._logger.info('profile: %r. %r', profile, profile.data)

        with open(model_path, 'rb') as input_fle:
            w, h, image = benbox_slicer.image_reader.read_image(input_fle)

        laser_values = benbox_slicer.conversion.on_off(image, w, h, threshold=128)
        del image

        # 0,0 is normally at the bottom left so we flip the data
        laser_values.reverse()

        with open(machinecode_path, 'w') as output_file:
            benbox_slicer.gcode.write_gcode(
                output_file,
                w, h,
                laser_values=laser_values,
                resolution=profile.data.get('resolution', 10),
                speed=profile.data.get('speed', 20),
            )

        self._logger.info('Sliced!')

        return True, dict(
            analysis={}
        )

    def cancel_slicing(self, path):
        self._logger.info("Cancel slicing")