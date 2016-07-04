# hello-pyrust

A “Hello World” of calling Rust code from a Python program with CFFI,
in order to show packaging issues.


## Build instructions

As-is, to build and run this demo:

* (Optional) Create a virtualenv and activate it.
* Run `pip install -e .` to install the [CFFI] dependency.
* Run `cargo build --manifest-path ./rust/Cargo.toml` to build Rust code and create a dynamic library.
* Run `python ./hello_pyrust.py` to run a program that uses CFFI’s ABI mode
  to load (`dlopen()`) and call this library.

[CFFI]: https://cffi.readthedocs.io/en/latest/overview.html
