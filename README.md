# Lit-Checker

[![ci](https://github.com/catalinnega/lit-checker/workflows/CI/badge.svg)](https://github.com/catalinnega/lit-checker/actions/workflows/ci.yaml)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

computer vision experiment

## Installation
### Camera configuration (Tapo c100)
On the tapo app, go to camera settings and find the account username, password and device IP.

On your router, enable port forwarding on port 554 (DNS app -> TCP -> internal port=554, external port=554, internal_host=<your_camera_IP>)

You should open the 554 port on the firewall.


```sh
pip install lit-checker
```

## Usage

```python
import lit-checker
# TODO
```

## Links

- [Documentation](https://catalinnega.github.io/lit-checker)
- [Changelog](https://github.com/catalinnega/lit-checker/releases)
- [Contributing](CONTRIBUTING.md)
