# Pyprofiler

## Installation

### Install from pypi


### Install from repo

In virtual environment, install the package from this directory with: `pip install .`

## Usage

### Setup

Create a python module that contains functions/methods that start with `profile_`.

```
usage: pyprofiler [-h] [-n NAME_OF_RUN] [-c COMPARE_WITH] [-v] pyprofile_file

positional arguments:
  pyprofile_file        Filename of pyprofile file to run profiling on
                        (must contain functions with names starting with "profile_")

options:
  -h, --help            show this help message and exit
  -n NAME_OF_RUN, --name_of_run NAME_OF_RUN
                        Name of this profiling run
  -c COMPARE_WITH, --compare_with COMPARE_WITH
                        Name of profiling run to compare with
  -v, --verbose         Show more info like stack strace for profiling
```

### Run profiler

Run profiler and output data to file 'profiling_results.yml'. 

`pyprofiler -n <NAME_OF_RUN> <PYPROFILE_FILE>`

### Compare runs

Compare a run to a different run that is already stored in 'profiling_results.yml'

`pyprofiler -n <NAME_OF_RUN> <PYPROFILE_FILE> -c <PREVIOUS_RUN_NAME>`