# Lit-Checker

[![ci](https://github.com/catalinnega/lit-checker/workflows/CI/badge.svg)](https://github.com/catalinnega/lit-checker/actions/workflows/ci.yaml)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

computer vision experiment (in progress)

## Installation
You can install the required python packages with '__poetry__' or '__pip__'. If you want, you can also run the __.devcontainer__ for a docker image with _python3.11_.
### Poetry
```sh
poetry shell
poetry install
```
### Pip
```sh
pip install -e .
```

### .devcontainer (Optional)

## Usage

### Camera recording
First, you should update the YAML config file with your camera __username__, __password__ and __IP__. For more details see [here](#camera-account-information-parsing). The configuration file is located in the __configs__ directory. For example _config_c100.yaml_ can be located here:
```sh
...
│━━ configs
    │━━━ c100
        │━━━ config_c100.yaml
│━━ docs
│━━ run
│━━ src
...
```
You can run a test using the following script:

```sh
python3 run/test.py --cfg configs/c100/config_c100.yaml
```
Importing the library in  python can be done as follows:
```python
import lit-checker
# TODO
```

### Data annotation
Convert your video to images to create a video-images folder:
```bash
video-toimg your_video_file ## # this creates your_video_file/ directory
```

Run the annotation tool on your video-images folder:
```bash
labelme your_video_directory --label your_labels.txt --nodata --keep-prev
```

## Camera account information parsing
### Camera configuration (Tapo c100)
- On the tapo app, go to camera settings and find the account username, password and device IP;

- On your router, enable port forwarding on port 554 (DNS app -> TCP -> internal port=554, external port=554, internal_host=<your_camera_IP>);

- You should open the 554 port on the firewall.

## References
 Data annotation: [Image Polygonal Annotation with Python
](https://github.com/labelmeai/labelme)

## Links
- [Documentation](https://catalinnega.github.io/lit-checker)
- [Changelog](https://github.com/catalinnega/lit-checker/releases)
- [Contributing](CONTRIBUTING.md)
