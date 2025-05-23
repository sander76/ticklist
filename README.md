![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/sander76/a25f1e6bfcb3b085ffe05f520b56e43c/raw/covbadge.json)
[![PyPI - Version](https://img.shields.io/pypi/v/clipstick.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/clipstick/)
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black)

# Ticklist

Ticklist is a Python library designed to create interactive forms based on Pydantic models using the Textual framework. It provides a seamless way to generate user interfaces for data entry and editing, leveraging the power of Pydantic for data validation and Textual for building rich, interactive applications.

## Features

- **Pydantic Integration**: Automatically generate forms based on Pydantic models.
- **Textual Widgets**: Use Textual's widgets to create a responsive and interactive user interface.
- **Annotation Handling**: Supports various Pydantic annotations, including `str`, `int`, `Enum`, `Literal`, `Union`, and more.
- **Custom Annotations**: Define custom annotations to control the behavior and appearance of form fields.
- **Validation**: Automatically validate user input using Pydantic's validation rules.

## Installation

You can install Ticklist using pip:

```bash
pip install ticklist
```

## Usage

A simple example of how to use Ticklist to create a form for a Pydantic model:

```python
{{include "example.py"}}
```

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
