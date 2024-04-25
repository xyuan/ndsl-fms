========
Overview
========

Quick Start
------------
Recommended Python is `3.11.x` all other dependencies will be pulled during install.

NDSL submodules `gt4py` and `dace` to point to vetted versions, use `git clone --recurse-submodule`.

NDSL is __NOT__ available on `pypi`. Installation of the package has to be local, via `pip install ./NDSL` (`-e` supported). The packages has a few options:

- `ndsl[test]`: installs the test packages (based on `pytest`)
- `ndsl[develop]`: installs tools for development and tests.

Tests are available via:

- `pytest -x test`: running CPU serial tests (GPU as well if `cupy` is installed)
- `mpirun -np 6 pytest -x test/mpi`: running CPU parallel tests (GPU as well if `cupy` is installed)

Requirements & supported compilers
----------------------

For CPU backends:

- 3.11.x >= Python < 3.12.x
- Compilers:
  - GNU 11.2+
- Libraries:
  - Boost headers 1.76+ (no lib installed, just headers)

For GPU backends (the above plus):

- CUDA 11.2+
- Python package:
  - `cupy` (latest with proper driver support [see install notes](https://docs.cupy.dev/en/stable/install.html))
- Libraries:
  - MPI compiled with cuda support

Configurations for Pace
----------------------------

Pace uses the following configurations for choice of NDSL
- FV3_DACEMODE=Python[Build|BuildAndRun|Run] controls the full program optimizer behavior
  - Python: default, use stencil only, no full program optmization
  - Build: will build the program then exit. This _build no matter what_. (backend must be `dace:gpu` or `dace:cpu`)
  - BuildAndRun: same as above but after build the program will keep executing (backend must be `dace:gpu` or `dace:cpu`)
  - Run: load pre-compiled program and execute, fail if the .so is not present (_no hashs check!_) (backend must be `dace:gpu` or `dace:cpu`)
- PACE_FLOAT_PRECISION=64 control the floating point precision throughout the program.
