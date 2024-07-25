from dataclasses import dataclass, field


@dataclass
class GoogleDriveUploaderConfig:
    client_json_file_path: str = field(
        default="service-secrets.json",
        metadata={"help": "the service-secrets.json file downloaded from Google API Console"})
    google_drive_root_folder: str = field(
        default="lit-checker",
        metadata={"help": "The root Google Drive folder name\
                   shared with the Google service account"})
