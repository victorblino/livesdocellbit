from dataclasses import dataclass
import os

@dataclass(frozen=True)
class BotConfig:
    twitch_app_id: str
    twitch_app_secret: str
    webhook_url: str
    twitter_consumer_key: str
    twitter_consumer_secret: str
    twitter_access_token: str
    twitter_access_token_secret: str
    streamer_username: str
    
    @staticmethod
    def load_from_env() -> 'BotConfig':
        def get(name: str, required: bool = True) -> str:
            value = os.getenv(name)
            if required and not value:
                raise ValueError(f"Environment variable '{name}' is required but not set.")
            return value or ""
        return BotConfig(
            twitch_app_id=get('TWITCH_APP_ID'),
            twitch_app_secret=get('TWITCH_APP_SECRET'),
            webhook_url=get('WEBHOOK_URL'),
            twitter_consumer_key=get('TWITTER_CONSUMER_KEY'),
            twitter_consumer_secret=get('TWITTER_CONSUMER_SECRET'),
            twitter_access_token=get('TWITTER_ACCESS_TOKEN'),
            twitter_access_token_secret=get('TWITTER_ACCESS_TOKEN_SECRET'),
            streamer_username=get('STREAMER_USERNAME')
        )