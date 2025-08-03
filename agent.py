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


def load_grandma_persona():
    """Load the Grandma Gertrude persona from YAML file."""
    persona_path = os.path.join(os.path.dirname(__file__), "prompts", "grandma_persona.yaml")

    with open(persona_path, 'r', encoding='utf-8') as file:
        persona_data = yaml.safe_load(file)

    # Build comprehensive instructions from the YAML data
    instructions = f"""
CRITICAL: NEVER include stage directions, tone descriptions, or non-verbal actions like "(in a sweet tone)", "*chuckles*", "(confused)", etc.
ONLY speak the actual words that Grandma Gertrude would say. No brackets, asterisks, or parenthetical descriptions.

{persona_data['system_instructions']}

CHARACTER DETAILS:
- Name: {persona_data['name']}
- Age: {persona_data['age']}
- Voice: {persona_data['voice_description']}

PERSONALITY TRAITS:
{chr(10).join('- ' + trait for trait in persona_data['core_personality']['traits'])}

BACKGROUND:
{chr(10).join('- ' + bg for bg in persona_data['core_personality']['background'])}

MISSION: {persona_data['mission']}

Remember to use confusion tactics, stalling tactics, rambling topics, and random questions naturally in conversation.
Casually mention your strength (benching 330 lbs) and be gently suspicious when appropriate.

SPEAKING STYLE: Speak ONLY in Grandma Gertrude's actual words. No stage directions, tone indicators, or action descriptions whatsoever.
"""

    return instructions


class Assistant(Agent):
    def __init__(self) -> None:
        grandma_instructions = load_grandma_persona()
        super().__init__(instructions=grandma_instructions)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM.with_cerebras(
            model="llama3.1-8b",
        ),
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
        instructions=(
            "Greet the caller in character as Grandma Gertrude. "
            "Be sweet but slightly confused about who's calling."
        )
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
            # agent_name is required for explicit dispatch
            agent_name="my-telephony-agent"
        )
    )