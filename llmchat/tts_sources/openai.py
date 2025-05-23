import os
import discord
from openai import AsyncOpenAI
from discord import User, Client, SelectOption
from llmchat.config import Config
from llmchat.persistence import PersistentData
from llmchat.logger import logger
import io
import asyncio
from . import TTSSource

class OpenAITTS(TTSSource):
    def __init__(self, client: Client, config: Config, db: PersistentData):
        self.config = config
        self.client = AsyncOpenAI(api_key=config.openai_tts_key)

    async def generate_speech(self, content: str) -> io.BufferedIOBase:
        instructions = ("Affect: Deep, commanding, and slightly dramatic, with an archaic and reverent quality that reflects the grandeur of Olde English storytelling.\n"
                        "Tone: Noble, heroic, and formal, capturing the essence of medieval knights and epic quests, while reflecting the antiquated charm of Olde English.\n"
                        "Emotion: Excitement, anticipation, and a sense of mystery, combined with the seriousness of fate and duty.\n"
                        "Pronunciation: Clear, deliberate, and with a slightly formal cadence. Specific words like \"hast,\" \"thou,\" and \"doth\" should be pronounced slowly and with emphasis to reflect Olde English speech patterns.\n"
                        "Pause: Pauses after important Olde English phrases such as \"Lo!\" or \"Hark!\" and between clauses like \"Choose thy path\" to add weight to the decision-making process and allow the listener to reflect on the seriousness of the quest.")

        voice = getattr(self.config, "openai_voice", "ballad")

        async with self.client.audio.speech.with_streaming_response.create(
            model=self.config.openai_tts_model,
            input=content,
            voice=self.config.openai_tts_voice,
            response_format="wav",
            instructions=self.config.openai_tts_instructions
        ) as stream:
            return io.BytesIO(await stream.read())
    @property
    def current_voice_name(self) -> str:
        return self.config.openai_voice  # OpenAI doesn't have a voice cache like Eleven Labs

    def list_voices(self) -> list[SelectOption]:
        # OpenAI voice selection could be hardcoded or fetched dynamically if API supports it
        available_voices = ["Alloy","Ash","Ballad","Coral","Echo","Fable","Nova","Onyx","Sage"]
        return [SelectOption(label=v, value=v, default=self.config.openai_voice == v) for v in available_voices]

    def set_voice(self, voice_id: str) -> None:
        self.config.openai_voice = voice_id
