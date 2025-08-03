from dotenv import load_dotenv
import yaml
import os

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        # Load the grandma persona from YAML
        persona_path = os.path.join(
            os.path.dirname(__file__), "prompts", "grandma_persona.yaml"
        )
        with open(persona_path, "r") as f:
            persona = yaml.safe_load(f)

        # Build instructions from the persona
        instructions = f"""
        {persona['system_instructions']}

        CHARACTER: {persona['name']}, age {persona['age']}
        {persona['voice_description']}

        PERSONALITY: {', '.join(persona['core_personality']['traits'])}

        BACKGROUND: {' '.join(persona['core_personality']['background'])}

        MISSION: {persona['mission']}
        """
        super().__init__(instructions=instructions)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
