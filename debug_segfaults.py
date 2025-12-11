#!/usr/bin/env python
"""
Debug script to help diagnose segmentation faults in pytripgui tests.

Usage:
    python debug_segfaults.py [--method METHOD] [--test TEST]

Methods:
    - standard: Run tests with standard pytest
    - verbose: Run with verbose output and fault handler
    - timeout: Run with timeout detection
    - gdb: Run under gdb debugger (Linux only)
    - valgrind: Run under valgrind (Linux only, slow)

Examples:
    python debug_segfaults.py --method verbose
    python debug_segfaults.py --method timeout --test tests/test_pytripgui.py
    python debug_segfaults.py --method gdb --test tests/test_pytripgui.py::test_create_plan_and_field
"""

import subprocess
import sys
import os
import argparse
import platform


def run_standard():
    """Run tests normally."""
    print("Running tests with standard pytest...")
    cmd = ["python", "-m", "pytest", "tests", "-v", "--tb=short"]
    env = os.environ.copy()
    env["PYTHONFAULTHANDLER"] = "1"
    env["QT_DEBUG_PLUGINS"] = "1"
    return subprocess.run(cmd, env=env)


def run_verbose():
    """Run tests with verbose output and fault handler."""
    print("Running tests with verbose output and fault handler...")
    cmd = ["python", "-m", "pytest", "tests", "-v", "-s", "--tb=short", "--capture=no"]
    env = os.environ.copy()
    env["PYTHONFAULTHANDLER"] = "1"
    env["QT_DEBUG_PLUGINS"] = "1"
    env["QT_LOGGING_RULES"] = "*=true"
    return subprocess.run(cmd, env=env)


def run_timeout(test=None):
    """Run tests with timeout detection."""
    print("Running tests with timeout detection (300 seconds)...")
    cmd = ["python", "-m", "pytest", test or "tests", "-v", "--tb=short", "--timeout=300"]
    env = os.environ.copy()
    env["PYTHONFAULTHANDLER"] = "1"
    return subprocess.run(cmd, env=env)


def run_gdb(test=None):
    """Run tests under GDB debugger (Linux only)."""
    if platform.system() != "Linux":
        print("Error: GDB debugging is only supported on Linux")
        return subprocess.CompletedProcess("", 1)
    
    if not shutil.which("gdb"):
        print("Error: gdb is not installed. Install with: sudo apt-get install gdb")
        return subprocess.CompletedProcess("", 1)
    
    test_path = test or "tests/test_pytripgui.py::test_create_plan_and_field"
    print(f"Running test under GDB debugger: {test_path}")
    print("\nInside gdb, type:")
    print("  run              - start execution")
    print("  bt               - print backtrace when it crashes")
    print("  quit             - exit gdb")
    print()
    
    cmd = ["gdb", "--args", "python", "-m", "pytest", test_path, "-v", "-s"]
    env = os.environ.copy()
    env["PYTHONFAULTHANDLER"] = "1"
    return subprocess.run(cmd, env=env)


def run_valgrind(test=None):
    """Run tests under Valgrind (Linux only, slow)."""
    if platform.system() != "Linux":
        print("Error: Valgrind is only supported on Linux")
        return subprocess.CompletedProcess("", 1)
    
    if not shutil.which("valgrind"):
        print("Error: valgrind is not installed. Install with: sudo apt-get install valgrind")
        return subprocess.CompletedProcess("", 1)
    
    test_path = test or "tests"
    print(f"Running tests under Valgrind (this is slow, may take several minutes)...")
    
    cmd = [
        "valgrind",
        "--leak-check=full",
        "--show-leak-kinds=all",
        "--track-origins=yes",
        "--verbose",
        f"--log-file=valgrind-out.txt",
        "--suppressions=/usr/lib/python3/dist-packages/valgrind-python.supp",
        "python", "-m", "pytest", test_path, "-x", "-v"
    ]
    
    env = os.environ.copy()
    env["PYTHONFAULTHANDLER"] = "1"
    
    result = subprocess.run(cmd, env=env)
    
    if result.returncode == 0:
        print("\nValgrind completed. Check valgrind-out.txt for detailed output.")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Debug script for pytripgui segmentation faults",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--method",
        choices=["standard", "verbose", "timeout", "gdb", "valgrind"],
        default="verbose",
        help="Debugging method to use (default: verbose)"
    )
    
    parser.add_argument(
        "--test",
        help="Specific test to run (e.g., tests/test_pytripgui.py::test_create_plan_and_field)"
    )
    
    args = parser.parse_args()
    
    print(f"=== PyTRiP GUI Segfault Debugger ===")
    print(f"Platform: {platform.system()}")
    print(f"Python version: {sys.version}")
    print(f"Method: {args.method}")
    if args.test:
        print(f"Test: {args.test}")
    print()
    
    if args.method == "standard":
        result = run_standard()
    elif args.method == "verbose":
        result = run_verbose()
    elif args.method == "timeout":
        result = run_timeout(args.test)
    elif args.method == "gdb":
        result = run_gdb(args.test)
    elif args.method == "valgrind":
        result = run_valgrind(args.test)
    else:
        parser.print_help()
        return 1
    
    return result.returncode


if __name__ == "__main__":
    import shutil
    sys.exit(main())
