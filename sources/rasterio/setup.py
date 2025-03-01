import os

from setuptools import find_packages, setup

description = 'A rasterio tilesource for large_image.'
long_description = description + '\n\nSee the large-image package for more details.'


def prerelease_local_scheme(version):
    """
    Return local scheme version unless building on master in CircleCI.

    This function returns the local scheme version number
    (e.g. 0.0.0.dev<N>+g<HASH>) unless building on CircleCI for a
    pre-release in which case it ignores the hash and produces a
    PEP440 compliant pre-release version number (e.g. 0.0.0.dev<N>).
    """
    from setuptools_scm.version import get_local_node_and_date

    if os.getenv('CIRCLE_BRANCH') in ('master',):
        return ''
    else:
        return get_local_node_and_date(version)


try:
    from setuptools_scm import get_version

    version = get_version(root='../..', local_scheme=prerelease_local_scheme)
    limit_version = f'>={version}' if '+' not in version else ''
except (ImportError, LookupError):
    limit_version = ''

setup(
    name='large-image-source-rasterio',
    use_scm_version={
        'root': '../..',
        'local_scheme': prerelease_local_scheme,
        'fallback_version': 'development',
    },
    setup_requires=['setuptools-scm'],
    description=description,
    long_description=long_description,
    license='Apache Software License 2.0',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        f'large-image{limit_version}',
        'rasterio>=1.3',  # to get the statistics attribute (<=> gdalinfo)
        'packaging',
    ],
    extras_require={
        'girder': f'girder-large-image{limit_version}',
        'all': [
            'rio-cogeo',
            'pydantic<2',
        ],
    },
    keywords='large_image, tile source',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/large_image',
    python_requires='>=3.8',
    entry_points={
        'large_image.source': [
            'rasterio = large_image_source_rasterio:RasterioFileTileSource'
        ],
        'girder_large_image.source': [
            'rasterio = large_image_source_rasterio.girder_source:RasterioGirderTileSource'
        ],
    },
)
