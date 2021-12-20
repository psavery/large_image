import os

from setuptools import find_packages, setup

description = 'An OMETiff tilesource for large_image.'
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

    if os.getenv('CIRCLE_BRANCH') in ('master', ):
        return ''
    else:
        return get_local_node_and_date(version)


setup(
    name='large-image-source-ometiff',
    use_scm_version={'root': '../..', 'local_scheme': prerelease_local_scheme},
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'large-image',
        'large-image-source-tiff>=1.0.0',
    ],
    extras_require={
        'girder': 'girder-large-image',
    },
    keywords='large_image, tile source',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/large_image',
    python_requires='>=3.6',
    entry_points={
        'large_image.source': [
            'ometiff = large_image_source_ometiff:OMETiffFileTileSource'
        ],
        'girder_large_image.source': [
            'ometiff = large_image_source_ometiff.girder_source:OMETiffGirderTileSource'
        ]
    },
)
