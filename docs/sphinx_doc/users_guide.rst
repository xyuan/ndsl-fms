Users Guide
=============

1: Introduction
----------------
Recently, Python has became the dominant programming language in machine learning and data sciences community since it is easy to learn and program, however the performance of Python is still the major concern in scientific computing and HPC community. In scientific computing and HPC community, the most widely used programming language is C/C++ and Fortran, Python is often used as script language for pre- and post-processing. Although, many complains about Python program performance happened from time to time, and obviously, Python program community didn't take it seriously for the language standard consideration. 

The major performance issue in Python programming language, especially in computation-intensive applications, are loops, which are often the performance bottlenecks of an application in other programming languages too, such as C++ and Fortran. However, Python program often observes 10x to 100x slower than C, C++ and Fortran program. In order to achieve peak hardware performance, the scientific computing community have tried different programming model, such as OpenMP, Cilk+, Thread Building Blocks (TBB) as well as Linux p-threads for multi/many-core processors and GPUs, and Kokkos, RAJA, OpenMP offload, and OpenACC for highest performance on CPU/GPUs heterogeneous system, all these programming models are only available for C, C++ and Fortran. Only a few works that targets to high perfromance for Python programming language.

The Python based NDSL programming model described in this users guide provides an alternative solution to reach peak hardware performance with relatively little programming effort by using the stencil semantics. A stencil is similar to parallel for kernel that used in Kokkos and RAJA, to update array elements according to a fixed access pattern. With the stencil semantics in mind, NDSL, for example, can be used to write matrix multiplication kernels that match the performance of cuBLAS/hipBLAS that many GPU programmers can’t do in Cuda/HiP using only about 30 lines of code. NDSL has already been used in Pace global climate model, which achieves up to 4x speedup, more efficient than the original Fortran implementations. 

2: Programming model
----------------------------------------------------
The programming model of NDSL is composed of backend execution Spaces, optimization pass and transformations, and memory spaces, memory layout. These abstraction semantics allow the formulation of generic algorithms and data structures which can then be mapped to different types of hardware architectures. Effectively, they allow for compile time transformation of algorithms to allow for adaptions of varying degrees of hardware parallelism as well as of the memory hierarchy. Figure 1 shows the high level architecture of NDSL, the AST visitor (the NDSL/external/gt4py/src/gt4py/cartesian/frontend/gtscript_frontend.py) IRMaker class traverses the AST of a python function decorated by @gtscript.function and stencil objects, and generates the corresponding definition IR.

.. 1:

.. figure:: static/ndsl_flow.png
   :width: 860
   :align: center

   The High-level architecture of NDSL.

From Fig. 1, we know that NDSL uses hierarchy levels intermediate representation (IR) to abstract the structure of computational program, whcih reduces the complexity of application program, and maintenance cost, while the code portability and scalability are increased. It also avoids raising the information from lower level representations by means of static analysis, and memory leaking, where feasible, and performaing optimizations at the high possible level of abstraction. The methods primarily leverages structural information readily available in the source code, it enables to apply the optimization, such as loop fusion, tiling and vectorization without the need for complicated analysis and heuristics.

In NDSL, the original Python AST of the program is then transform to the Definition IR, the definition IR is high level IR, and composed of high level program information, domain-specific information, and the structure of computational operations. It allows to transform the IR while avoiding the performance cliffs of numerical libraries, but it doesn't contains detailed information that required for performance on specific hardware. The definition IR, particularly, only preserve the necessary information to lower operations to hardware instructions implementing coarse-grained vector operations, or to numerical libraries — such as cuBLAS/hipBLAS and Intel MKL. 


The definition IR is then transformed to GTIR, which is used for backend for code generator for GridTools. The analysis is also performed on the GTIR to remove the redunant nodes, and prunning the unused parameters, and data type and shape propogations of the symbols, and loop extensions. 


The GTIR is then transoformed to optimization IR (OIR), performation optimization algorithm are carried out based on OIR by developing pass/transorformations. Currently, the vertical loop merging, and horizonal loop mergy, and loop unrolling and vectorization, statement fusion and pruning optimizations are available and activated by the environmental variable in the oir_pipeline module. 


After the optimization pipeline finished, the OIR is then converted to different backend IR, for example, DACE IR (SDFG). The DACE SDFG can be further optimizated by its embeded pass/transormations algorithm, but in PACE application, we didn't activate this optimization step. 

