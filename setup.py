from setuptools import setup
from setuptools import find_packages

VERSION = '0.1dev'

requires = [
    'fabric',
]

setup(name='portl',
      version=VERSION,
      description='Tethr Buildr',
      author="Chris Rossi",
      author_email="chris@archimedeanco.com",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      build = buildr:main
      [buildr.builds]
      portl = buildr.builds.portl:PortlBuild
      """)
