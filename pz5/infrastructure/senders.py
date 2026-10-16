class EmailSender:
    def send(self, message: str) -> None:
        print(f"[Email] Відправлено: {message}")

class SmsSender:
    def send(self, message: str) -> None:
        print(f"[SMS] Відправлено: {message}")