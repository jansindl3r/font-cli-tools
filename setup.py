from setuptools import setup, find_packages

setup(
    name='font_cli_tools',
    version='0.1',
    packages=find_packages(),
    description='Font ClI Tools',
    author='Jan Sindler',
    author_email='jansindl3r@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='fonts, cli, tools, plugin',
    python_requires='>=3.6',
    install_requires=[
        'drawbot-skia',
        'defcon',
        'fontTools',
        'booleanOperations'
    ],
    entry_points={
        'console_scripts': [
            'plot_font=font_cli_tools.plot_font:main',
            'remove_non_exporting_glyphs=font_cli_tools.remove_non_exporting_glyphs:main',
            'remove_rvrn_glyphs=font_cli_tools.remove_rvrn_glyphs:main',
            'rename_bracket_layers=font_cli_tools.rename_bracket_layers:main',
            'remove_overlaps=font_cli_tools.remove_overlaps:main',
            'decompose_transformed_glyphs=font_cli_tools.decompose_transformed_glyphs:main',
            'decompose_glyphs=font_cli_tools.decompose_glyphs:main',
        ],
    }
)