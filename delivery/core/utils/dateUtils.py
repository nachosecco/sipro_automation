class dateUtils:
    def toSeconds(self, time: str):
        """Convert seconds from HH:MM:SS to seconds."""
        h, m, s = time.split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)
