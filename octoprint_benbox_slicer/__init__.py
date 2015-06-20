from octoprint_benbox_slicer.plugin import BenboxSlicer, png_file_support

__plugin_implementation__ = BenboxSlicer()
__plugin_hooks__ = {
    'octoprint.filemanager.extension_tree': png_file_support
}
