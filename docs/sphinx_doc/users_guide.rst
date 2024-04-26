Users Guide
=============

How to accelerate Python code by 100x using NDSL
----------------------------------------------------
Python has become the dominant programming language in machine learning and data sciences community because it is easy to learn and program, however the performance of Python is still the major concern in scientific computing community. In scientific community, the most widely used programming language is C/C++ and Fortran, Python is often used as script language for pre- and post-processing. The complains about Python program performance from time to time, and Python should certainly not take all the blame. Still, it's fair to say that Python's nature as an interpreted language does not help, especially in computation-intensive scenarios (e.g., when there are multiple nested for loops).

If you were ever caught up in one of the following situations, then this article is definitely for you.

It takes forever to run a massive for loop in my Python program...
My program has a bottleneck at some computation tasks. Rewriting the code in C++ and calling C++ with the ctypes module can work, but it's not straightforward enough and risks compilation failures when the code is transplanted to other devices. It would be much better if I could keep all the work done in a Python script.
I am a loyal C++/Fortran user but would like to try out Python as it is gaining increasing popularity. However, rewriting code in Python is a nightmare - I feel the performance must be more than 100x slower than before!
I need to process lots of images, and OpenCV cannot give me what I want. So I have to write nested loops manually. This is not very enjoyable.
If you can relate, then you might want to learn more about Taichi. For those who have not heard of Taichi: Taichi is a DSL embedded in Python but has its own compiler to take over the code decorated with @ti.kernel, achieving high-performance execution on all kinds of hardware, including CPU and GPU. One of the most notable advantages it delivers is speeding up Python code, hence no need to envy the performance of C++/CUDA any more. (See the benchmark report.)

The developers in the Taichi community put a lot of effort into improving Taichi's compatibility with Python. So far, all Taichi features can function perfectly after you import taichi as ti; You can easily install Taichi via the pip install command and interact with other Python libraries, including NumPy, Matplotlib, and PyTorch.

I am not exaggerating when I say Taichi can be your solution. In this blog, I'm going to explain how Taichi manages to accelerate Python code by at least 50 times through three examples:

Count the number of primes less than N
Find the longest common subsequence (LCS) via dynamic programming
Solve reaction-diffusion equations
A shortcut to the source code of the three cases: https://github.com/taichi-dev/faster-python-with-taichi.
