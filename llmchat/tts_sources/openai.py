import os
import discord
import openai
from discord import SelectOption
import io
import asyncio
from . import TTSSource

class OpenAITTS(TTSSource):
    async def generate_speech(self, content: str) -> io.BufferedIOBase:
        openai.api_key = self.config.openai_key  # Ensure your OpenAI API key is set
        instructions = """Affect: Deep, commanding, and slightly dramatic, with an archaic and reverent quality that reflects the grandeur of Olde English storytelling.\n\nTone: Noble, heroic, and formal, capturing the essence of medieval knights and epic quests, while reflecting the antiquated charm of Olde English.\n\nEmotion: Excitement, anticipation, and a sense of mystery, combined with the seriousness of fate and duty.\n\nPronunciation: Clear, deliberate, and with a slightly formal cadence. Specific words like \"hast,\" \"thou,\" and \"doth\" should be pronounced slowly and with emphasis to reflect Olde English speech patterns.\n\nPause: Pauses after important Olde English phrases such as \"Lo!\" or \"Hark!\" and between clauses like \"Choose thy path\" to add weight to the decision-making process and allow the listener to reflect on the seriousness of the quest."""
        response = await self.client.loop.run_in_executor(None, lambda: openai.Audio.create(
            model="gpt-4o-mini-tts",
            input=content,
            voice="ballad",
            instructions=instructions
        ))

        buf = io.BytesIO(response["audio"])  # OpenAI returns audio as bytes
        return buf

    @property
    def current_voice_name(self) -> str:
        return self.config.openai_voice  # OpenAI doesn't have a voice cache like Eleven Labs

    def list_voices(self) -> list[SelectOption]:
        # OpenAI voice selection could be hardcoded or fetched dynamically if API supports it
        available_voices = ["Alloy","Ash","Ballad","Coral","Echo","Fable","Nova","Onyx","Sage"]
        return [SelectOption(label=v, value=v, default=self.config.openai_voice == v) for v in available_voices]

    def set_voice(self, voice_id: str) -> None:
        self.config.openai_voice = voice_id
