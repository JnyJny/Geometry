'''setup for Geometry

'''

from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here,'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='Geometry',
      version='0.0.0',
      description = 'Geometry the python way.',
      long_description = long_description,
      url = 'https://github.com/JnyJny/Geometry',
      author="Erik O'Shaughnessy",
      author_email="erik.oshaughnessy@gmail.com",
      license='MIT',
      classifiers=[ 'Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: Scientific/Engineering :: Mathematics',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.4'],
      keywords = 'geometry point circle line segment triangle rectangle graph',
      packages = find_packages(exclude=['contrib','docs','tests']),
      install_requires = [],
      extras_require = {},
      package_data = {},
      data_files= [],
)


