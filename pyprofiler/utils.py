import sys
import importlib.util
from pathlib import Path
import yaml

def read_yml_file(path: str) -> dict:
    """Get results from previous profiling runs"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return dict(yaml.safe_load(f))
    except (FileNotFoundError, TypeError):
        return {}


def write_yml_file(path: str, data: dict) -> None:
    with open(path, 'w', encoding='utf8') as f:
        yaml.dump(data, f)


def load_module(filename: str):
    """Load subclasses of `parent_class_name` from given filename module"""
    module_name = Path(filename).stem
    spec = importlib.util.spec_from_file_location(module_name, filename)
    assert spec, f"No parseable module in {filename}"

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module
