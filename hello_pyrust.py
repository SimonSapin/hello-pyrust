import os.path
from cffi import FFI


ffi = FFI()
ffi.cdef("""
    int hello(const char *who);
""");

# FIXME: path is hard-coded, .so is OS-specific
lib = os.path.join(os.path.dirname(__file__), 'rust', 'target', 'debug', 'libhello_pyrust.so')

rust = ffi.dlopen(lib)


def main():
    assert rust.hello(b"Python") == 42


if __name__ == '__main__':
    main()
