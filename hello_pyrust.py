import os.path
import sys
from cffi import FFI


ffi = FFI()
ffi.cdef(open(os.path.join(
    # FIXME: path is hard-coded
    os.path.dirname(__file__), 'rust', 'src',
    'hello_pyrust.h',
)).read());

if sys.platform == 'win32':
    DYNAMIC_LIB_FORMAT = '%s.dll'
elif sys.platform == 'darwin':
    DYNAMIC_LIB_FORMAT = 'lib%s.dylib'
# FIXME: Does this need to check for other values of `sys.platform`?
else:
    DYNAMIC_LIB_FORMAT = 'lib%s.so'

rust_lib = ffi.dlopen(os.path.join(
    # FIXME: path is hard-coded
    os.path.dirname(__file__), 'rust', 'target', 'debug',
    DYNAMIC_LIB_FORMAT % 'hello_pyrust'
))


def main():
    assert rust_lib.hello(b"Python") == 42


if __name__ == '__main__':
    main()
