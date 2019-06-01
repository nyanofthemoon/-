from setuptools import setup

setup(
  name='nu',
  version='0.2.0',
  packages=['nu'],
  author='Nyan Of The Moon',
  author_email='nyanofthemoon@gmail.com',
  description='Framework for creating Anki Vector skills using additional sensory inputs.',
  url='https://hotchiwawa.com',
  license='MIT',
  entry_points={
      'console_scripts': [
          'nu = nu.__main__:main'
      ]
  },
  install_requires=[
      'anki_vector',
      'configparser',
      'redis',
      'hiredis',
      'sense-hat',
      'flask',
      'pyopenssl'
  ],
  zip_safe=False
)
