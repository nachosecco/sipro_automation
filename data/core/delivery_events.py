class DeliveryEvents:
    def __init__(self, events):
        self.events = events

    def media(self, media_name):
        return [e for e in self.events if e.data.media_name == media_name]
