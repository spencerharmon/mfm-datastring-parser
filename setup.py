from setuptools import setup, find_namespace_packages

setup(
    name="mfm_griddata_parser",
    version="0.1",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    test_suite="tests.test",
    author="Spencer Harmon",
    author_email="the.spencer.harmon@gmail.com",
    description="Parses griddata output from MFM (patch in beta)",
    keywords="MFM Ulam artificial life",
    url="http://www.github.com/spencerharmon/mfm-griddata-parser",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ]
)
