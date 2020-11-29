from distutils.util import convert_path
from setuptools import setup, find_packages


package_name = 'renderable-box'

package_directory = package_name.replace('-', '_')
package_info = {}

with open(convert_path(f'{package_directory}/package.py'), 'r') as file:
  exec(file.read(), package_info)

requirements = [
  'renderable-core@git+https://f2df37d2224599278c1adf7ba248ea3589a85448:x-oauth-basic@github.com/therenderable/renderable-core.git'
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
