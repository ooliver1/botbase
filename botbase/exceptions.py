from nextcord import DiscordException


class Blacklisted(DiscordException):
    def __init__(self, message: str):
        self.message: str = message
