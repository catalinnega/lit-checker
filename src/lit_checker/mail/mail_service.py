import logging
import smtplib
from email.message import EmailMessage

from lit_checker.logging import LogConfig, get_logger
from lit_checker.mail.args import MailAccountConfig, MailServiceConfig, MailTypesConfig


class MailService:
    def __init__(self, config: MailServiceConfig, logger: logging.Logger | None):
        if logger is not None:
            self.log = logger
        else:
            self.log = get_logger(LogConfig())
        self.config = config
        self.mail_type_config: MailTypesConfig = self.config.mail_types
        self.mail_account_config: MailAccountConfig = self.config.account

    def send_mail(
            self,
            mail_title_type: str,
            mail_content_type: str,
            mail_content: str) -> None:
        smtp_sender = self.__init_smtp_sender(
            self.mail_account_config.address,
            self.mail_account_config.password,
        )

        mail_title = self.mail_type_config.__dict__[mail_title_type]
        mail_content_prefix = self.mail_type_config.__dict__[mail_content_type]
        message = EmailMessage()
        message['To'] = self.mail_account_config.to_address
        message['From'] = self.mail_account_config.address
        message['CC'] = self.mail_account_config.address
        message['Subject'] = mail_title

        body = f"{mail_content_prefix}\n{mail_content}"
        message.set_content(body)
        smtp_sender.send_message(message)
        smtp_sender.quit()
        self.log.info(
            f"Sent message to {self.mail_account_config.to_address} succesfully")

    def __init_smtp_sender(self, mail_address: str, mail_password: str) -> smtplib.SMTP:
        smtp_sender = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_sender.starttls()
        smtp_sender.login(mail_address, mail_password)
        return smtp_sender


if __name__ == '__main__':
    config = MailServiceConfig()
    config.account.address = 'address@gmail.com'
    config.account.to_address = 'address@gmail.com'
    config.account.password = 'address'

    mail_service = MailService(config, logger=None)

    mail_content = 'hello'
    mail_service.send_mail(
        mail_title_type='motion_detection_title',
        mail_content_type='motion_detection_content',
        mail_content=mail_content
    )
