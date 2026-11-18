"""Used while real email is NOT set up: prints emails in the terminal.
Unlike Django's default, it never crashes on characters the terminal cannot show (₱, ñ, etc.)."""
from django.conf import settings
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend


class SafeConsoleEmailBackend(ConsoleEmailBackend):
    def write_message(self, message):
        text = message.message().as_bytes().decode(message.encoding or settings.DEFAULT_CHARSET)
        text = f"{text}\n{'-' * 79}\n"
        enc = getattr(self.stream, "encoding", None) or "utf-8"
        self.stream.write(text.encode(enc, "replace").decode(enc))
