from dataclasses import dataclass

@dataclass
class StreamState:
    """
    Represents the current state of the stream, including whether it's online, the current game being played, and the stream title.
    """
    
    online: bool = False
    current_game: str = ""
    stream_title: str = ""
    
    def reset_for_offline(self):
        """
        Resets the stream state to default values when the stream goes offline.
        """
        self.online = False
    
    def update_from_update(self, update: dict):
        self.online = update.get('online', self.online)
        self.current_game = update.get('current_game', self.current_game)
        self.stream_title = update.get('stream_title', self.stream_title)
    