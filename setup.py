from distutils.command.install import install
from setuptools import setup, find_packages

app_dependencies = [
    "ilb-pycontext==2.2.2",
    "bottle==0.12.18",
    "gunicorn==20.0.4",
    "opencv-python==4.6.0.66",
    "pylibdmtx==0.1.10",
    "numpy~=1.19.5",
    "pdf2image~=1.16.3",
    "debugpy==1.4.1",
]


class RunApplicationCommand(install):

    def run(self):
        import debugpy
        debugpy.listen(('0.0.0.0', 8888))

        import dmtxrecogn.__main__
        dmtxrecogn.__main__.main()


setup(
    name="dmtxrecogn",
    version="1.0.0",
    url="https://github.com/ilb/dmtxrecogn",
    description="Service for datamatrix recognition",
    author="Alexander Kiyan",
    author_email="ssortia@gmail.com",
    packages=find_packages(exclude=["test.*", "test"]),
    python_requires=">=3.6",
    install_requires=app_dependencies,
    # extras_require={"dev": dev_dependencies, },
    package_data={"": ["*.json", "*.yaml", "*.xml"]},
    entry_points={"console_scripts": ["dmtxrecogn=dmtxrecogn.__main__:main", ], },
    cmdclass={'run': RunApplicationCommand}
)
