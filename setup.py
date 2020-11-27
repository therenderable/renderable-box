from distutils.util import convert_path
from setuptools import setup, find_packages


package_name = 'renderable-box'

package_directory = package_name.replace('-', '_')
package_info = {}

with open(convert_path(f'{package_directory}/package.py'), 'r') as file:
  exec(file.read(), package_info)

requirements = [
  'psutil>=5.7.0',
  'requests>=2.25.0',
  'pydantic>=1.7.0',
  'pymongo>=3.11.0',
  'pika>=1.1.0'
]

entrypoints = {
  'console_scripts': [
    f'{package_name} = {package_directory}.cli.__main__:main'
  ]
}

setup(
  name = package_name,
  version = package_info['__version__'],
  description = package_info['__description__'],
  author = package_info['__author__'],
  author_email = package_info['__email__'],
  license = package_info['__license__'],
  python_requires = '>=3.7.0',
  install_requires = requirements,
  packages = find_packages(),
  entry_points = entrypoints,
  zip_safe = False)
