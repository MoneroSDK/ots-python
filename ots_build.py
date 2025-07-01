from argparse import ArgumentParser
from tempfile import TemporaryDirectory
from cffi import FFI
from pathlib import PurePath
from os import path, makedirs
from re import sub, DOTALL
from sys import exit


LIBS = [
    'monero-ots',
    'epee',
    'easylogging',
    'monero-crypto',
    'monero-stubs',
    'utf8proc'
]  # Names of the library to link against (e.g., -lmonero-ots...)
CDEF_HEADER_FILES = [
    'include/ots.h',
    'include/ots-errors.h'
]  # C header files to generate CFFI cdef from (e.g., ots.h, ots-errors.h)


class FfiBuilderController(FFI):
    """
    Controller for FFI Builder to manage the building process.
    """
    def __init__(self,
        library_path=None,
        include_path=None,
        library=None,
        output_dir=None,
        cdef_header_file=None,
        temp=None,
        debug=False,
        args=None
    ):
        self.library_path = library_path or []
        self.include_path = include_path or []
        self.library = library or LIBS
        self.output_dir = output_dir or path.join(path.dirname(__file__), "ots")
        self.cdef_header_file = cdef_header_file or CDEF_HEADER_FILES
        self.temp = temp or None
        self.debug = debug
        if args is not None:
            self.parse_args(args)
        super().__init__()
        self.cdef(
            self.generate_cdef_from_header()
        )
        self.set_source(
            "ots._ots",  # Name of the generated C module
            self.generate_source(),  # C source code to compile
            libraries=self.library,  # Libraries to link against
            library_dirs=self.library_path,  # Directories to search for libraries
            include_dirs=self.include_path,  # Directories to search for header files
        )

    def parse_args(self, args):
        """
        Parses command line arguments.
        """
        self.library_path = args.library_path or self.library_path
        self.include_path = args.include_path or self.include_path
        self.library = args.library or self.library
        self.output_dir = args.output_dir or self.output_dir
        self.cdef_header_file = args.cdef_header_file or self.cdef_header_file
        self.temp = args.temp or self.temp
        self.debug = args.debug if hasattr(args, 'debug') else self.debug

    def compile(self):
        """
        Compiles the FFI module.
        """
        if self.temp is None:
            td = TemporaryDirectory(prefix='ots_temp_')
            self.temp = td.name
        if not path.exists(self.output_dir):
            makedirs(self.output_dir)
        if self.debug:
            print(f"""
            Debug mode enabled
            Library paths: {', '.join(self.library_path)}
            Include paths: {', '.join(self.include_path)}
            Libraries to link: {', '.join(self.library)}
            Output directory: {self.output_dir}
            C header files: {', '.join(self.cdef_header_file)}
            Temporary directory: {self.temp}
            """)
            print("Compiling the FFI module...")
        super().compile(
            verbose=self.debug,
            target=path.join(self.output_dir, "_ots.so"),
            tmpdir=self.temp
        )

    def cdef_from_header(self, header_file: str) -> str:
        """Loads the C header file content to create cdef, filtering out unwanted content."""
        with open(header_file, 'r') as f:
            header_content = f.read()
            f.close()
            # Remove #include lines
            header_content = sub(r'#include .*\n', '', header_content)
            # Remove #ifdef __cplusplus blocks
            header_content = sub(r'#ifdef __cplusplus\nextern "C" {\n', '', header_content)
            header_content = sub(r'#ifdef __cplusplus\n}\n', '', header_content)
            header_content = sub(r'#endif\s*//.*?\n', '', header_content) # Handle potential comments on #endif
            # Remove multi-line comment blocks /* ... */
            header_content = sub(r'\s*/\*.*?\*/', '', header_content, flags=DOTALL)
            # Remove single-line comments // ...
            header_content = sub(r'//.*?\n', '', header_content)
            # Remove #ifndef <XXX> blocks
            header_content = sub(r'#ifndef .*?\n#define .*?\n', '', header_content)
            header_content = sub(r'#ifndef .*?\n', '', header_content)
            # Remove #define <XXX>
            header_content = sub(r'#endif\s*//.*?\n', '', header_content)
            header_content = sub(r'#endif.*', '', header_content)
            # Remove empty lines
            header_content = sub(r'\n\s*\n', '\n', header_content)
            header_content = sub(
                r'^(.*)inline(\s.*\(.*\))\s?{.*}',
                r'\1\2;',
                header_content,
                flags=DOTALL
            )  # Remove inline function bodies
            return header_content
        raise OSError(f"Could not read header file: {header_file}")

    def generate_cdef_from_header(self) -> str:
        """
        Generates C definitions from a list of header files.
        """
        cdef_content = ''
        for header in self.cdef_header_file:
            cdef_content += self.cdef_from_header(header) + '\n'
        if self.debug:
            with open('ots_cdef.h', 'w') as f:
                f.write(cdef_content)
                f.close()
        return cdef_content

    def generate_source(self) -> str:
        source_content = ""
        for inlude in self.cdef_header_file:
            include_path = PurePath(inlude).name
            source_content += f'#include <{include_path}>\n'
        if self.debug:
            with open('source.c', 'w') as f:
                f.write(source_content)
                f.close()
        return source_content

if __name__ == '__main__':
    parser = ArgumentParser(description='Build the OTS CFFI module.')
    parser.add_argument(
        '--library-path',
        '-p',
        nargs='+',
        default=None,
        help='Path to the directory containing the OTS library (e.g., libots.so or libots.dll).'
    )
    parser.add_argument(
        '--include-path',
        '-i',
        nargs='+',
        default=None,
        help='Path to the directory containing the OTS header files (e.g., ots.h).'
    )
    parser.add_argument(
        '--library',
        '-l',
        nargs='+',
        default=None,
        help='Name of the OTS library to link against (e.g., ots, epee, easylogging, monero-crypto, monero-stubs, utf8proc).'
    )
    parser.add_argument(
        '--output-dir',
        '-d',
        default=None,
        help='Directory to output the compiled module (default: ots/).'
    )
    parser.add_argument(
        '--cdef-header-file',
        '-c',
        nargs='*',
        default=None,
        help='C header files to generate CFFI cdef from (default: include/ots.h, include/ots-errors.h).'
    )
    parser.add_argument(
        '--temp',
        '-t',
        default=None,
        help='Temporary directory for building the OTS CFFI module (default: a temporary directory).'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='Enable debug mode for verbose output.'
    )
    ffibuilder = FfiBuilderController(args=parser.parse_args())
    ffibuilder.compile()
    exit(0)


ffibuilder = FfiBuilderController()
