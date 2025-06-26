from sys import argv, exit
from cffi import FFI
import cffi
import os
import re

ffibuilder = FFI()

# C definitions for CFFI
# We extract this directly from the header, with minor adjustments for CFFI if needed.
# Note: CFFI cannot parse `#include` directly in cdef.
# Static inline functions like ots_handle_valid are not directly usable via cdef;
# their logic would be reimplemented in Python or they'd need to be non-static.
# For simplicity, we'll declare functions and let Python wrappers handle logic.
def load_header(header_file):
    """Loads the C header file content, filtering out unwanted content."""
    try:
        with open(header_file, 'r') as f:
            header_content = f.read()
            f.close()
            # Remove #include lines
            header_content = re.sub(r'#include .*\n', '', header_content)
            # Remove #ifdef __cplusplus blocks
            header_content = re.sub(r'#ifdef __cplusplus\nextern "C" {\n', '', header_content)
            header_content = re.sub(r'#ifdef __cplusplus\n}\n', '', header_content)
            header_content = re.sub(r'#endif\s*//.*?\n', '', header_content) # Handle potential comments on #endif
            # Remove multi-line comment blocks /* ... */
            header_content = re.sub(r'\s*/\*.*?\*/', '', header_content, flags=re.DOTALL)
            # Remove single-line comments // ...
            header_content = re.sub(r'//.*?\n', '', header_content)
            # Remove #ifndef <XXX> blocks
            header_content = re.sub(r'#ifndef .*?\n#define .*?\n', '', header_content)
            header_content = re.sub(r'#ifndef .*?\n', '', header_content)
            # Remove #define <XXX>
            # header_content = re.sub(r'#define .*?\n', '', header_content)
            # Remove #endif lines (including potential comments after #endif)
            header_content = re.sub(r'#endif\s*//.*?\n', '', header_content)
            header_content = re.sub(r'#endif.*', '', header_content)
            # Remove empty lines
            header_content = re.sub(r'\n\s*\n', '\n', header_content)
            header_content = re.sub(
                r'^(.*)inline(\s.*\(.*\))\s?{.*}',
                r'\1\2;',
                header_content,
                flags=re.DOTALL
            )  # Remove inline function bodies
            return header_content
    except FileNotFoundError:
        print(f"Error: Header file '{header_file}' not found.")
        exit(1)

CDEF_SOURCE = load_header("include/ots.h") + load_header("include/ots-errors.h")
with open("ots_cdef.h", "w") as f:
    f.write(CDEF_SOURCE)

ffibuilder.cdef(CDEF_SOURCE)

# Source for CFFI to compile.
# This includes the header and specifies the library to link against.
# It can also include helper C functions if needed for GC or complex argument conversions.
# For functions taking `X**` that need to be GC'd with `X*`, helpers are useful.
# Example: static void _gc_helper_free_string(char *s) { if (s) ots_free_string(&s); }
# This is not strictly necessary for all `X**` free functions if the Python side manages
# the `X*` and constructs `X*[]` or `&X*` for the call.
# For `ots_free_handle_object`, it takes `ots_handle_t*`, which is simpler for GC.

SOURCE = """
#include "ots.h"
#include "ots-errors.h"
"""

ffibuilder.set_source(
    "_ots",  # Name of the generated C module
    SOURCE,
    libraries=[
        'monero-ots',
        'epee',
        'easylogging',
        'monero-crypto',
        'monero-stubs',
        'utf8proc'
    ],  # Name of the library to link against (e.g., -lots)
    library_dirs = [ # Add if libots.so/dll or other libs are not in standard linker paths
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib'),
        argv[1]
    ],
    include_dirs = [ # Add if ots.h or other header files are not in standard include paths
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'include'),
        argv[2]
    ],
)
if __name__ == "__main__":
    if len(argv) < 3:
        exit(1)
    print("Building OTS CFFI module...")
    output_dir = os.path.join(os.path.dirname(__file__), "ots")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # CFFI will generate files in the current directory by default.
    # To put them in a subdirectory, you can temporarily change directory
    # or handle paths carefully if CFFI allows specifying output path for generated C file.
    # For simplicity, this example assumes CFFI generates files in the script's dir.
    # Or, you can tell CFFI to put the .o and .so files in a specific location
    # using ffibuilder.compile(target="path/to/module.so", tmpdir="build_temp")

    ffibuilder.compile(verbose=True, target=os.path.join(output_dir, "_ots.so"), tmpdir=output_dir)
