import setuptools

setuptools.setup(
    name="aiohq",
    version="0.0",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    license="MIT",
    python_requires=">=3.9",
    install_requires=[
        'aiohttp',
    ],
    entry_points=dict(
        console_scripts=[
            'aiohq = aiohq.__main__:main',
        ]
    ),
    extras_require={
        'dev': [
            'aiohttp-devtools',
        ],
    }
)
