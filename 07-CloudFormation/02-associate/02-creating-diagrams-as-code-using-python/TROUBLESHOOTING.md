# Troubleshooting Guide

This document provides solutions to common issues encountered during the setup and execution of the VPC Diagram project using the `diagrams` Python library.

## Table of Contents

- [Virtual Environment Issues](#virtual-environment-issues)
    - [Virtual Environment Not Activating](#virtual-environment-not-activating)
    - [Python Packages Not Recognized](#python-packages-not-recognized)
- [Graphviz Installation Issues](#graphviz-installation-issues)
- [Script Execution Issues](#script-execution-issues)
- [Other Common Issues](#other-common-issues)
    - [Incorrect Python Interpreter](#incorrect-python-interpreter)
    - [Python Packages Not Recognized](#missing-dependencies)
- [Conclusion](#conclusion)
- [References](#references)

## Virtual Environment Issues

### Virtual Environment Not Activating

**Problem:** The virtual environment does not activate, or the command prompt does not show the virtual environment name.

**Solution:**

1. Deactivate any currently active virtual environments:

```bash
deactivate
```

2. Ensure you are using the correct path to activate the virtual environment:

```bash
source /path/to/your/project/myenv/bin/activate
```

3. If you still face issues, check for aliases that might override the `python` command:

```bash
alias
```

If `python` is aliased to a different interpreter, remove the alias:

```bash
unalias python
```

### Python Packages Not Recognized

**Problem:** Python packages such as `diagrams` are not recognized, leading to `ModuleNotFoundError`.

**Solution:**

1. Ensure the virtual environment is activated:

```bash
source myenv/bin/activate
```

2. Verify the Python interpreter is from the virtual environment:

```bash
which python
```

The output should point to the virtual environment path, e.g., `/path/to/your/project/myenv/bin/python`.
3. List installed packages to confirm `diagrams` is installed:

```bash
pip list
```

If `diagrams` is not listed, install it:

```bash
pip install diagrams
```

## Graphviz Installation Issues

**Problem:** Graphviz is not installed or not found, leading to errors when generating diagrams.

**Solution:**

1. Install Graphviz using Homebrew:

```bash
brew install graphviz
```

2. Verify Graphviz installation by checking its version:

```bash
dot -V
```
This should display the version of Graphviz installed.

## Script Execution Issues

**Problem:** Running the Python script results in errors, such as `ModuleNotFoundError` or issues related to the virtual environment.

**Solution:**

1. Ensure the virtual environment is activated before running the script:

```bash
source myenv/bin/activate
```

2. Run the script using the correct Python interpreter:

```bash
python vpc_diagram.py
```

If issues persist, explicitly specify the Python interpreter from the virtual environment:

```bash
/path/to/your/project/myenv/bin/python vpc_diagram.py
```

## Other Common Issues

### Incorrect Python Interpreter

**Problem:** The Python interpreter points to the system Python instead of the virtual environment.

**Solution:**

1. Check the current Python interpreter:

```bash
which python
```

2. Ensure it points to the virtual environment path. If not, activate the virtual environment correctly:

```bash
source myenv/bin/activate
```

### Missing Dependencies

**Problem:** Dependencies are missing, leading to import errors.

**Solution:**

1. Ensure all required packages are installed:

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt` file, manually install the necessary packages:

```bash
pip install diagrams
```

## Conclusion

This troubleshooting guide addresses common issues encountered during the setup and execution of the VPC Diagram project. By following the provided solutions, you should be able to resolve most issues and successfully generate the VPC architecture diagram.

## References

- [Diagrams Documentation](https://diagrams.mingrammer.com/)
- [Graphviz Documentation](https://graphviz.org/documentation/)
- [Python Documentation](https://docs.python.org/3/)

