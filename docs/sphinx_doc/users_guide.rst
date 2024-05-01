Users Guide
=============

1: Introduction
----------------
Recently, Python has became the dominant programming language in machine learning and data sciences community since it is easy to learn and program, however the performance of Python is still the major concern in scientific computing and HPC community. In scientific computing and HPC community, the most widely used programming language is C/C++ and Fortran, Python is often used as script language for pre- and post-processing. Although, many complains about Python program performance happened from time to time, and obviously, Python program community didn't take it seriously in the language standard consideration. 

The major performance issue in Python programming language, especially in computation-intensive applications, are loops, which are often the performance bottlenecks of an application in other programming languages too, such as C++ and Fortran. However, Python program often observes 10x to 100x slower than C, C++ and Fortran program. In order to achieve peak hardware performance, the scientific computing community have tried different programming model, such as OpenMP, Cilk+, Thread Building Blocks (TBB) as well as Linux p-threads for multi/many-core processors and GPUs, and Kokkos, RAJA, OpenMP offload, and OpenACC for highest performance on CPU/GPUs heterogeneous system, all these programming models are only available for C, C++ and Fortran. Only a few works that target to high perfromance for Python programming language.

The Python based NDSL programming model described in this users guide provides an alternative solution to reach peak hardware performance with relatively little programming effort by using the stencil semantics. A stencil is similar to parallel for kernel that used in Kokkos and RAJA, to update array elements according to a fixed access pattern. With the stencil semantics in mind, NDSL, for example, can be used to write matrix multiplication kernels that match the performance of cuBLAS/hipBLAS that many GPU programmers can’t do in Cuda/HiP using only about 30 lines of code. It greatly reduces the programmer's effort, and NDSL has already been successfully used in Pace global climate model, which achieves up to 4x speedup, more efficient than the original Fortran implementations. 

2: Programming model
----------------------------------------------------
The programming model of NDSL is composed of backend execution spaces, performance optimization pass and transformations, and memory spaces, memory layout. These abstraction semantics allow the formulation of generic algorithms and data structures which can then be mapped to different types of hardware architectures. Effectively, they allow for compile time transformation of algorithms to allow for adaptions of varying degrees of hardware parallelism as well as of the memory hierarchy. Figure 1 shows the high level architecture of NDSL, From Fig. 1, it is shown that NDSL uses hierarchy levels intermediate representation (IR) to abstract the structure of computational program, whcih reduces the complexity of application code, and maintenance cost, while the code portability and scalability are increased. It also avoids raising the information from lower level representations by means of static analysis, and memory leaking, where feasible, and performaing optimizations at the high possible level of abstraction. The methods primarily leverages structural information readily available in the source code, it enables to apply the optimization, such as loop fusion, tiling and vectorization without the need for complicated analysis and heuristics.

.. 1:

.. figure:: static/ndsl_flow.png
   :width: 860
   :align: center

   The High-level architecture of NDSL.


In NDSL, the AST visitor (the NDSL/external/gt4py/src/gt4py/cartesian/frontend/gtscript_frontend.py) IRMaker class traverses the AST of a python function decorated by @gtscript.function and stencil objects, the Python AST of the program is then transform to the Definition IR. The definition IR is high level IR, and is composed of high level program, domain-specific information, and the structure of computational operations which are independent of low level hardware platform. The definition of high level IR allows transformation of the IRs without lossing the performance of numerical libraries. But the high level IR doesn't contains detailed information that required for performance on specific low level runtime hardware. Specificially, the definition IR only preserves the necessary information to lower operations to runtime platform hardware instructions implementing coarse-grained vector operations, or to numerical libraries — such as cuBLAS/hipBLAS and Intel MKL. 


The definition IR is then transformed to GTIR (gt4py/src/gt4py/cartesian/frontend/defir_to_gtir.py), the GTIR stencils is defined as in NDSL

.. code-block:: none

   class Stencil(LocNode, eve.ValidatedSymbolTableTrait):
       name: str
       api_signature: List[Argument]
       params: List[Decl]
       vertical_loops: List[VerticalLoop]
       externals: Dict[str, Literal]
       sources: Dict[str, str]
       docstring: str

       @property
       def param_names(self) -> List[str]:
           return [p.name for p in self.params]

       _validate_lvalue_dims = common.validate_lvalue_dims(VerticalLoop, FieldDecl)



GTIR contains `vertical_loops` loop statement, in the climate applications, the vertical loops usually need special treatment as the numerical unstability is arison. The `vertical_loops` in GTIR as separate code block help the following performance pass and transofrmation implementation. The program analysis pass/transformation is performed on the GTIR to remove the redunant nodes, and prunning the unused parameters, and data type and shape propogations of the symbols, and loop extensions. GTIR is also used for backend code generation if the gridtools backend is chosen.


The GTIR is then transoformed to optimization IR (OIR), performation optimization algorithm are carried out based on OIR by developing pass/transorformations. Currently, the vertical loop merging, and horizonal loop mergy, and loop unrolling and vectorization, statement fusion and pruning optimizations are available and activated by the environmental variable in the oir_pipeline module. 


After the optimization pipeline finished, the OIR is then converted to different backend IR, for example, DACE IR (SDFG). The DACE SDFG can be further optimizated by its embeded pass/transormations algorithm, but in PACE application, we didn't activate this optimization step. 

