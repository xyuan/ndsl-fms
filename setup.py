import os
import sys
import multiprocessing
from pathlib import Path
from typing import List

from setuptools import find_namespace_packages, setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext

def get_cmake_args():
    import shlex

    num_threads = os.getenv("BUILD_NUM_THREADS", multiprocessing.cpu_count())
    cmake_args = shlex.split(os.getenv("FMS_CMAKE_ARGS", "").strip())

    use_msbuild = False
    use_xcode = False

    if os.getenv("DEBUG", "0") in ("1", "ON"):
        cfg = "Debug"
    elif os.getenv("RELWITHDEBINFO", "0") in ("1", "ON"):
        cfg = "RelWithDebInfo"
    elif os.getenv("MINSIZEREL", "0") in ("1", "ON"):
        cfg = "MinSizeRel"
    else:
        cfg = None
    build_options = []
    if cfg:
        build_options.extend(["--build-type", cfg])
    if sys.platform == "win32":
        if os.getenv("FMS_USE_MSBUILD", "0") in ("1", "ON"):
            use_msbuild = True
        if use_msbuild:
            build_options.extend(["-G", "Visual Studio 17 2022"])
        else:
            build_options.extend(["-G", "Ninja", "--skip-generator-test"])
    if sys.platform == "darwin":
        if os.getenv("FMS_USE_XCODE", "0") in ("1", "ON"):
            use_xcode = True
        if use_xcode:
            build_options.extend(["-G", "Xcode", "--skip-generator-test"])
    sys.argv[2:2] = build_options

    if sys.platform == "darwin" and use_xcode:
        os.environ["BUILD_OPTIONS"] = f"-jobs {num_threads}"
    elif sys.platform != "win32":
        os.environ["BUILD_OPTIONS"] = f"-j{num_threads}"
    elif use_msbuild:
        # /M uses multi-threaded build (similar to -j)
        os.environ["BUILD_OPTIONS"] = f"/M"
    if sys.platform == "darwin":
        if platform.machine() == "arm64":
            cmake_args += ["-DCMAKE_OSX_ARCHITECTURES=arm64"]
        else:
            cmake_args += ["-DCMAKE_OSX_ARCHITECTURES=x86_64"]
    # netcdf setup
    cmake_args +=["-DNetCDF_INCLUDE_DIRS=/usr/local/lib/netcdf-4.6.1/include -DCMAKE_VERBOSE_MAKEFILE=ON"]            
    return cmake_args


class CMakeExtension(Extension):
    """
      extension class for cmake build of FMS
    """
    def __init__(self, name):
        super().__init__(name, sources=[])


class BuildExt(build_ext):
    """
    defined build_ext for cmake and make build of FMS
    """
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = Path().absolute()

        build_temp = f"{Path(self.build_temp)}/{ext.name}"
        os.makedirs(build_temp, exist_ok=True)
        extdir = Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        cmake_args = get_cmake_args()

        config = "Debug" if self.debug else "Release"
        build_args = [
            "--config", config,
            "--", "-j8"
        ]

        os.chdir(build_temp)
        self.spawn(["cmake", f"{str(cwd)}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(str(cwd))


def local_pkg(name: str, relative_path: str) -> str:
    """Returns an absolute path to a local package."""
    path = f"{name} @ file://{Path(os.path.abspath(__file__)).parent / relative_path}"
    return path

# fms cmake setup
fms = CMakeExtension("external/FMS")

test_requirements = ["pytest", "pytest-subtests"]
develop_requirements = test_requirements + ["pre-commit"]

extras_requires = {"test": test_requirements, "develop": develop_requirements}

requirements: List[str] = [
    local_pkg("gt4py", "external/gt4py"),
    local_pkg("dace", "external/dace"),
    "mpi4py==3.1.5",
    "cftime",
    "xarray",
    "f90nml>=1.1.0",
    "fsspec",
    "netcdf4",
    "scipy",  # restart capacities only
    "h5netcdf",  # for xarray
    "dask",  # for xarray
    "cffi",
]


setup(
    author="NOAA/NASA",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=requirements,
    extras_require=extras_requires,
    name="ndsl",
    license="BSD license",
    packages=find_namespace_packages(include=["ndsl", "ndsl.*"]),
    include_package_data=True,
    url="https://github.com/NOAA-GFDL/NDSL",
    version="2024.04.00",
    zip_safe=False,
    ext_modules=[fms],  # for fms cmake build
    cmdclass={"build_ext": BuildExt} # use defined build_ext
)
