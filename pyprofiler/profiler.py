"""Classes used in PyProfiler"""

from __future__ import annotations

import cProfile
from datetime import datetime
import pstats
import time
import timeit
import logging

from pyprofiler.utils import load_module, read_yml_file, write_yml_file
from pyprofiler.color import Color, text_in_color

HISTORY_FILE = "profiling_results.yml"
logger = logging.getLogger(__name__)


class PyProfiler:
    """Run profiling on methods"""

    def __init__(self, name=None, verbose=False):
        self.timestamp = round(time.time())
        self.name = (
            name or datetime.strftime(datetime.now(), "%Y-%m-%d-%H:%M:%S")
        )
        self.verbose = verbose
        logger.info("Created PyProfiler with name %s", self.name)

    def get_function_identifier(self, fun):
        """Append module name with function name to create a unique
        string for each function that is profiled"""
        module_name = fun.__module__
        function_name = fun.__qualname__
        return f"{module_name or ''}:{function_name}"

    def pyprofile(
            self,
            fun,
            *args,
            store_results=True,
        ):
        """Run cProfile for a function with arguments given, print results"""

        function_identifier = self.get_function_identifier(fun)
        print(f"Profiling function {function_identifier}")

        # Run cProfile to see stack trace
        c_profiler = None
        if self.verbose:
            c_profiler = cProfile.Profile()
            c_profiler.enable()

        time_taken = timeit.Timer(
            lambda: fun(*args)
        ).timeit(number=1)

        print(
            f"\t Total time was "
            f"{round(time_taken, 8)}s"
        )

        if c_profiler:
            c_profiler.disable()
            stats = pstats.Stats(c_profiler)
            stats.sort_stats('cumtime').print_stats(10)

        if store_results:
            self.store_results(function_identifier, time_taken)

    def store_results(self, function_name, time_taken_avg) -> None:
        """Store the results from the profiling run"""
        results = read_yml_file(HISTORY_FILE)
        results.setdefault(self.name, {})
        results[self.name]["timestamp"] = self.timestamp
        results[self.name].setdefault("methods", {})
        results[self.name]["methods"][function_name] = time_taken_avg
        write_yml_file(HISTORY_FILE, results)
        print(f"Saved profiling run in {HISTORY_FILE}")

    def get_two_latest_runs(self):
        """Find the two latest ran profile names"""
        latest_run = {}
        latest_run_name = ""
        previous_latest_run = {}
        previous_latest_run_name = ""

        profile_runs = read_yml_file(HISTORY_FILE)
        for run_name, run in profile_runs.items():
            if run.get('timestamp') > latest_run.get("timestamp", -1):
                previous_latest_run = latest_run
                previous_latest_run_name = latest_run_name
                latest_run = run
                latest_run_name = run_name
            elif run.get('timestamp') > previous_latest_run.get("timestamp", -1):
                previous_latest_run = run
                previous_latest_run_name = run_name

        return previous_latest_run_name, latest_run_name

    @classmethod
    def format_time_diff_percentage(cls, diff_perc):
        """Set color for the command line text"""
        color = Color.OFF
        if diff_perc < -5:
            color = Color.GREEN
        elif diff_perc > 5:
            color = Color.RED

        diff_perc_string = f"{'+' if diff_perc > 0 else ''}{diff_perc}%"
        return text_in_color(diff_perc_string, color)

    @classmethod
    def compare_results(
        cls, profile_run_name_before, profile_run_name_after) -> None:
        """
        Compare results and print time difference between two profiling runs
        """

        profile_runs = read_yml_file(HISTORY_FILE)
        profile_run_before = profile_runs.get(
            profile_run_name_before, {}).get("methods", {})
        profile_run_after = profile_runs.get(
            profile_run_name_after, {}).get("methods", {})

        if not profile_run_before or not profile_run_after:
            raise LookupError(
                "Can not compare since there were no previous "
                "results to compare with"
            )

        print(
            "================================================================"
        )
        print(
            f"DIFF FROM {profile_run_name_before} TO {profile_run_name_after}"
        )

        for func_signature, duration_after in profile_run_after.items():
            try:
                duration_before = profile_run_before.get(func_signature)
                diff_perc = (
                    100 * (duration_after - duration_before) / duration_before
                )
                diff_perc_str = (
                    cls.format_time_diff_percentage(round(diff_perc, 2))
                )
                print(f"{func_signature}: {diff_perc_str}")

            except TypeError:
                # If one of the timestamps did not have the function
                print(
                    f"Failed to find function {func_signature} in previous run"
                )
                continue



def run_profiler(
    pyprofiler_file, requested_run_name: str, verbose=False
):
    """Create and run profiling with a PyProfiler file"""

    module = load_module(pyprofiler_file)
    profiler = PyProfiler(requested_run_name, verbose=verbose)

    for method_name in dir(module):

        if (method_name.startswith('profile_') and
            callable(getattr(module, method_name))):
            method = getattr(module, method_name)
            profiler.pyprofile(method)

    # Compare previous and current latest run
    run_name_before, run_name_after = profiler.get_two_latest_runs()

    try:
        profiler.compare_results(run_name_before, run_name_after)
    except LookupError:
        print("Could not compare since there were no previous run"
    )
