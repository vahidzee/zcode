from setuptools import setup, find_packages
from zcode import __version__

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zcode',
    packages=find_packages(include=['zcode', 'main' ]),  # add other exclusions in future
    version=__version__,
    license='MIT',
    description='Compress and decompress to and from `.zee` files!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vahid Zehtab',
    author_email='vahid98zee@gmail.com',
    url='https://github.com/vahidzee/zcode',
    keywords=['zcode', 'compression', 'lzw', 'lossless-compression'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Topic :: System :: Archiving :: Compression',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': ['zcode=zcode.main:main'],
    },
)
