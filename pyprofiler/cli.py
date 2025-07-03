import argparse
from pyprofiler.profiler import run_profiler

def cli():
    """CLI for PyProfiler - the easy profiler"""
    parser = argparse.ArgumentParser(
        description=(
            "PyProfiler - a profiling command line tool for python packages."
            "Can be used to run PyProfile files and compare profiling runs."
        )
    )
    parser.add_argument(
        '-n', '--name_of_run',
        type=str, help='Name of this profiling run'
    )
    parser.add_argument(
        '-c', '--compare_with',
        type=str, help='Name of profiling run to compare with'
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Show more info like stack strace for profiling",
        action='store_true'
    )
    parser.add_argument(
        'pyprofile_file', type=str,
        help=(
            'Filename of pyprofile file to run profiling on'
            '(must contain at least one class that inherits from PyProfile)'
        )
    )
    args = parser.parse_args()
    run_profiler(
        args.pyprofile_file,
        run_name=args.name_of_run,
        compare_with=args.compare_with,
        verbose=args.verbose
    )

if __name__ == "__main__":
    cli()
