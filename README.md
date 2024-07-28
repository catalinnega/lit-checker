# Lit-Checker

[![ci](https://github.com/catalinnega/lit-checker/workflows/CI/badge.svg)](https://github.com/catalinnega/lit-checker/actions/workflows/ci.yaml)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![Raspberry Pi Compatible](https://img.shields.io/badge/Raspberry%20Pi-Compatible-green)

Computer vision experiment (in progress)

## Current features:
 - Capturing Tapo C100 camera feed;
 - Applying motion detection and saving detection video;
 - Uploading detections to Google Drive and notifying the user via mail with the video link;
### In progress:
 - Personalized object detection using few-shot learning on manually annotated frames. (https://github.com/catalinnega/lit-checker-trainer).

## Installation
You can install the required python packages with '__poetry__' or '__pip__'. Optionally you can run the __.devcontainer__ for a docker image with _python3.11_.
### Poetry
```sh
poetry shell
poetry install
```
### Pip
```sh
pip install -e .
```

### Using .devcontainer (Optional)
To use a development container for a consistent development environment, follow these steps:
#### 1. Open the project in Visual Studio Code:
```sh
code .
```
#### 2. Reopen in Container:
 - Press F1 to open the command palette.
 - Type and select Remote-Containers: Reopen in Container.
This will build the container defined in .devcontainer and open the project inside it.


## Usage

### Run
To initialize the video feed capture routine, update the necessary configurations in the YAML file and run:
```bash
python3 run/run.py --cfg configs/c100/config_c100.yaml
``` 

### Camera recording configuration
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


## Camera account information parsing
### Camera configuration (Tapo c100)
- On the tapo app, go to camera settings and find the account username, password and device IP;

- On your router, enable port forwarding on port 554 (DNS app -> TCP -> internal port=554, external port=554, internal_host=<your_camera_IP>);

- You should open the 554 port on the firewall.

## Creating a service account from Google Drive API 
Creating a `service-secrets.json` file from the Google API Console involves setting up a service account and downloading the key in JSON format. Here are the detailed steps:

1. **Access the Google API Console**:
   - Go to the [Google API Console](https://console.developers.google.com/).

2. **Create a New Project**:
   - If you don’t have a project yet, click on the project dropdown (top-left corner) and select "New Project."
   - Fill in the required details and create the project.

3. **Enable the APIs**:
   - Select your project from the project dropdown.
   - Go to the "Library" in the sidebar.
   - Search for the API you need (e.g., Google Drive API, Google Sheets API) and click on it.
   - Click the "Enable" button to enable the API for your project.

4. **Create a Service Account**:
   - Navigate to "IAM & Admin" > "Service accounts" in the sidebar.
   - Click on "Create Service Account" at the top.
   - Fill in the details for your service account (name, ID, description).
   - Click "Create and Continue."

5. **Assign Roles to the Service Account**:
   - Choose the role(s) that your service account needs. For example, for Google Sheets API, you might choose "Editor."
   - Click "Continue."

6. **Create a Key for the Service Account**:
   - Click on "Done" after assigning roles.
   - In the "Service accounts" list, find the account you just created.
   - Click on the service account to edit it.
   - Go to the "Keys" tab.
   - Click "Add Key" > "Create New Key."
   - Select "JSON" as the key type and click "Create."

7. **Download the JSON Key File**:
   - The JSON key file will be downloaded automatically to your computer. This file contains your `service-secrets.json`.

8. **Store the JSON Key File Securely**:
   - Rename the downloaded file to `service-secrets.json` if needed.
   - Store this file securely and do not expose it publicly as it contains sensitive information.


Use this `service-secrets.json` file in your application to authenticate.

## Data annotation
For data annotation and subsequent model finetuning, use the 'lit-checker-trainer' project, which also manages the required packages for annotation:
```bash
git clone https://github.com/catalinnega/lit-checker-trainer
```

Alternatively, you can manually install 'video-cli' and 'labelme' packages to run the following commands:

-  Convert your video to images to create a video-images folder:
```bash
video-toimg your_video_file ## # this creates your_video_file/ directory
```

- Run the annotation tool on your video-images folder:
```bash
labelme your_video_directory --labels your_labels.txt --nodata --keep-prev
```

## Raspberry Pi Compatibility
This project is compatible with Raspberry Pi. It has been tested on Raspberry Pi 5 with the 'Ubuntu Server OS' image generated by Raspberry Pi Imager.

## References
 Data annotation: [Image Polygonal Annotation with Python
](https://github.com/labelmeai/labelme)

## Links
- [Documentation](https://catalinnega.github.io/lit-checker)
- [Changelog](https://github.com/catalinnega/lit-checker/releases)
- [Contributing](CONTRIBUTING.md)
