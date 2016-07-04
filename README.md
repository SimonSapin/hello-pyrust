# hello-pyrust

A “Hello World” of calling Rust code from a Python program with CFFI,
in order to show packaging issues.

**Note:** I’m using Rust here but the same could apply to other compiled languages:
replace `cargo build` with “an arbitrary command that produces a native dynamic library
that exports symbols with a C-compatible ABI and that CFFI can use with `dlopen()`”.


## Build instructions

As-is, to build and run this demo:

* (Optional) Create a virtualenv and activate it.
* Run `pip install -e .` to install the [CFFI] dependency.
* Run `cargo build --manifest-path ./rust/Cargo.toml` to build Rust code and create a dynamic library.
* Run `python ./hello_pyrust.py` to run a program that uses CFFI’s ABI mode
  to load (`dlopen()`) and call this library.
  This should print `Hello Python from Rust!` and not raise any exception.

[CFFI]: https://cffi.readthedocs.io/en/latest/overview.html


## What could be better (on the Python side)

The end-user has to run Cargo themselves
and the program only works when run from its source directory
because some paths are hard-coded.

Ideally, it should be relatively easy for library authors to write a `setup.py` file
that support three scenarios such that contributors and end-users don’t have to worry about
running Cargo as long as `cargo` and `rustc` executables can be found in `$PATH`.

* Development from the source directory:
  `pip install -e .` (or equivalent) runs Cargo automatically
  (and needs to be run again when the Rust source is changed).

* Distributing sources on PyPI:
  `python setup.py sdist` creates a distribution that includes the Rust source files,
  `Cargo.toml`, and the `.h` C headers file.
  When that distribution is installed (with `pip install` or equivalent),
  Cargo is run automatically
  and the Python program knows where to find the resulting dynamic library.

* Distributing binary builds (wheel files):
  `python setup.py bdist_wheel` runs Cargo automatically,
  and includes the resulting dynamic library in the wheel file.
  (Maybe the Rust source files don’t need to be included?)
  The wheel file is and is advertised as specific to one CPU architecture and operating system,
  but compatible with any Python version (including 2.x and 3.x).
  Cargo is *not* run when installing this wheel file,
  so that end-users don’t need to have cargo or rustc installed.


### Bonus points: cross-compilation

Assuming the proper toolchain is available (which admittedly can be tricky to install),
Cargo and Rust support compiling for a target (CPU architecture and operating system)
other than the one running the compiler.

When all of the above work well,
a next step would be to have some way to specify a cross-compilation target for binary builds.
`python setup.py bdist_wheel` would run Cargo with the appropriate `--target` parameter,
and create a wheel file with corresponding metadata and filename.


### I tried / Please help

Last year (in September 2015) I tried to achieve some of the above by monkey-patching distutils
and/or using a setuptools "entry point", based on blog posts from various people.
The result of that is at [SimonSapin/html5ever-python].
See [`setuptools_ext.py`] in particular.

[SimonSapin/html5ever-python]: https://github.com/SimonSapin/html5ever-python
[`setuptools_ext.py`]: https://github.com/SimonSapin/html5ever-python/blob/master/setuptools_ext.py

As far as I remember it mostly worked for development from the source directory,
but not for either distribution scenario.
I kinda got stuck after that.

Distutils internals are… let’s say not easy to work with.
And all support there for non-Python code seems to be specifically about
C code (*maybe* C++) using CPython’s C API with a compiler driven directly by distutils itself,
and nothing else.

If you know more about distutils (or Python packaging in general)
and are interested in making this better,
I’d love for you to file issues with details or send PRs.
Thanks!


## What could be better (on the Rust side)

I mostly made this repo to ask for help with Python packaging.
But for completeness, the Rust side of things could be improved as well.

In particular, the library’s ABI is duplicated
between the Rust source (used by rustc to build the dynamic library)
and the C header files (used by CFFI to know how to call the library).
Keeping in sync is important: a bug there could cause segfaults or security vulnerabilies.

Maybe the C header files could be generated automatically by a rustc compiler plugin,
sort of the opposite of [rust-bindgen].

[rust-bindgen]: https://github.com/servo/rust-bindgen
