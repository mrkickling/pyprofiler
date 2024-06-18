# Pyprofiler

## Usage


### Setup

Create a python module that contains a class which inherits from pyprofiler.profiler.PyProfiler.

Create methods that start with `profile_`.

The functions you want to profile in each method should be sent to `self.pyprofile` (with additional arguments). self.pyprofile takes a lambda/function/callable and arguments, and performs profiling on it.

usage: python3 -m pyprofiler [-h] {compare,profile}

### Run profiler

Run profiler (and show change in percentage from previous run)

`python3 -m pyprofiler profile [-h] [-n NAME_OF_RUN] [-v] pyprofile_file`

### Compare runs

Compare a run to a different run.

`python3 -m pyprofiler compare [-h] profile_run_name_before profile_run_name_after`