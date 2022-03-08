from setuptools import setup

setup(
    name='spectrolas',
    version='0.9.0',    
    description='Simple spectrum vizualizer',
    url='https://github.com/LucLabarriere/Spectrolas',
    author='Luc Labarrière',
    author_email='luc.labarriere@live.fr',
    license='MIT',
    packages=['spectrolas'],
    install_requires=['matplotlib',
                      'pyqt5',
					  'seabreeze',
					  'colorpy'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)
