from abc import ABC, abstractmethod


class LimiterInterface(ABC):
    @abstractmethod
    def can_send(user_id: int) -> bool:
        pass

class SenderInterface(ABC):
    @abstractmethod
    def send(self, subject: str, message: str, destination: str) -> None:
        pass


class ServiceInterface(ABC):
    @abstractmethod
    def send_verification_web(self, user_id: int, user_email: str, username:str, code: int) -> None:
        pass

    @abstractmethod
    def send_verification_telegram(self, user_id: int, user_email: str, username:str, code: int) -> None:
        pass
