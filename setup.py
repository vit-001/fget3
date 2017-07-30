from distutils.core import setup

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages = ['data_format/url','data_format/error','data_format/fl_data','data_format/history_data',
                'data_format/loader_error'],
    excludes = [],
    includes = ["atexit"],
    # include_files = ['resource/icon.png']
)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None
# base=None


setup(name='p_browser',
      version = '0.3.1',
      description = '',
      options = dict(build_exe = buildOptions, requires=['beautifulsoup4'])
      )
