import logging
import os

from lit_checker.drive.args import GoogleDriveUploaderConfig
from lit_checker.logging import LogConfig, get_logger
from lit_checker.mail.args import MailServiceConfig
from lit_checker.mail.mail_service import MailService
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GoogleDriveUploader:
    def __init__(
        self,
        config: GoogleDriveUploaderConfig,
        mail_config: MailServiceConfig,
        logger: logging.Logger | None,
    ):
        if logger is not None:
            self.log = logger
        else:
            self.log = get_logger(LogConfig())
        self.config = config
        self.authenticator = self.__login_with_service_account(config.client_json_file_path)
        self.drive_handler = self.__get_drive_handler(self.authenticator)
        self.folders_dict = self.init_gdrive_folders(
            config.google_drive_root_folder, folder_names=["motion_detections"]
        )
        self.mail_service = MailService(mail_config, logger=self.log)

    def upload_file_to_folder(self, file_path: str, folder_name: str) -> GoogleDrive | None:
        if folder_name in self.folders_dict:
            folder_file = self.folders_dict[folder_name]
            output_file_name = os.path.basename(file_path)
            file = self.drive_handler.CreateFile(
                {"parents": [{"id": folder_file["id"]}], "title": output_file_name}
            )
            file.SetContentFile(file_path)
            file.Upload()
            self.log.info(f"Uploaded at: {folder_file['title']}/{output_file_name}")
            self.send_mail_file_upload(file)
        else:
            file = None
        return None

    def send_mail_file_upload(self, file: GoogleDrive) -> None:
        mail_content = (
            f"File uploaded on Google Drive. You can access it at {file['alternateLink']}"
        )
        self.mail_service.send_mail(
            mail_title_type="motion_detection_title",
            mail_content_type="motion_detection_content",
            mail_content=mail_content,
        )

    def create_folder(self, folder_name: str, root_dir_id: str) -> GoogleDrive:
        file_metadata = {
            "title": folder_name,
            "parents": [{"id": root_dir_id}],  # parent folder
            "mimeType": "application/vnd.google-apps.folder",
        }

        folder = self.drive_handler.CreateFile(file_metadata)
        folder.Upload()
        return folder

    def create_folder_if_not_present(self, folder_name: str, root_dir_id: str) -> GoogleDrive:
        sub_files = self.drive_handler.ListFile(
            {"q": f"'{root_dir_id}' in parents and trashed=false"}
        ).GetList()

        folder_file = None
        if len(sub_files):
            self.log.info(f"Found sub_files in {root_dir_id}: {[f['title'] for f in sub_files]}")
            for sub_file in sub_files:
                if sub_file["title"] == folder_name:
                    folder_file = sub_file
                    break
        if folder_file is None:
            folder_file = gdrive_uploader.create_folder(
                folder_name=folder_name, root_dir_id=root_dir_id
            )
            self.log.info(f"Created folder 'motion_detections' in {root_dir_id}")
        return folder_file

    def init_gdrive_folders(
        self, google_drive_root_folder: str, folder_names: list[str]
    ) -> dict[str, GoogleDrive]:
        root_folders = self.drive_handler.ListFile().GetList()
        root_directory = google_drive_root_folder
        folder_files_dict: dict[str, GoogleDrive] = {}
        for root_folder_file in root_folders:
            for folder_name in folder_names:
                if root_folder_file["title"] == root_directory:
                    folder_file = self.create_folder_if_not_present(
                        folder_name=folder_name, root_dir_id=root_folder_file["id"]
                    )
                    folder_files_dict[folder_name] = folder_file
        return folder_files_dict

    def __login_with_service_account(self, client_json_file_path: str) -> GoogleAuth:
        settings = {
            "client_config_backend": "service",
            "service_config": {"client_json_file_path": client_json_file_path},
        }

        authenticator = GoogleAuth(settings=settings)
        authenticator.ServiceAuth()
        return authenticator

    def __get_drive_handler(self, authenticator: GoogleAuth) -> GoogleDrive:
        return GoogleDrive(authenticator)


if __name__ == "__main__":
    mail_config = MailServiceConfig()
    mail_config.account.address = "address@gmail.com"
    mail_config.account.to_address = "address@gmail.com"
    mail_config.account.password = "password"

    config = GoogleDriveUploaderConfig()
    config.client_json_file_path = "secrets.json"
    config.google_drive_root_folder = "lit-checker"
    gdrive_uploader = GoogleDriveUploader(config, mail_config, logger=None)
    print(gdrive_uploader.drive_handler)
    fpath = "/workspaces/lit-checker/lit_2024-07-25_17:18:02.mp4"
    gdrive_uploader.upload_file_to_folder(file_path=fpath, folder_name="motion_detections")
