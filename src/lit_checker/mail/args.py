from dataclasses import dataclass, field


@dataclass
class MailAccountConfig:
    address: str = field(default="account@gmail.com", metadata={"help": "Mail address"})
    password: str = field(default="password", metadata={"help": "Mail address password"})
    to_address: str = field(
        default="account@gmail.com", metadata={"help": "Mail address of mail recipient"}
    )


@dataclass
class MailTypesConfig:
    motion_detection_title: str = field(
        default="LitChecker Motion detection",
        metadata={"help": "Title of mail related to motion detection"},
    )
    motion_detection_content: str = field(
        default="Detected motion on:", metadata={"help": "Mail content beggining text"}
    )


@dataclass
class MailServiceConfig:
    account: MailAccountConfig = field(
        default_factory=MailAccountConfig, metadata={"help": "Mail account config"}
    )
    mail_types: MailTypesConfig = field(
        default_factory=MailTypesConfig, metadata={"help": "Mail types config"}
    )

    def __post_init__(self) -> None:
        self.account = MailAccountConfig(**self.account)  # type: ignore
        self.mail_types = MailTypesConfig(**self.mail_types.__dict__)
