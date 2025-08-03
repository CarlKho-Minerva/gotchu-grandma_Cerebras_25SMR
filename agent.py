import json
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


class ScamDetector:
    """Class to handle scam detection using Cerebras LLM."""

    def __init__(self, llm):
        self.llm = llm

    async def detect_scam_confidence(self, text):
        """Analyze text for scam confidence using Cerebras LLM."""
        try:
            # Create a chat context for the scam detection
            chat_ctx = agents.llm.ChatContext()
            chat_ctx.append(
                role="system",
                text="You are an expert scam detector. Analyze the text and respond with a JSON object containing scam confidence score, scam type, and reasoning.",
            )
            chat_ctx.append(
                role="user",
                text=f'Analyze the following text for scam likelihood on a scale from 0-100 where: 0 = definitely not a scam, 50 = neutral, uncertain, 100 = definitely a scam. Also identify the type of scam if detected. Text: "{text}" Respond ONLY with a JSON object in this format: {{"scam_confidence": <number between 0-100>, "scam_type": "<type of scam or \'unknown\' if not a scam>", "reasoning": "<brief explanation>"}}',
            )

            # Get response from LLM
            response = await self.llm.chat(chat_ctx=chat_ctx, temperature=0.3)

            # Parse the JSON response
            result = json.loads(response.choices[0].message.content)
            return (
                result.get("scam_confidence", 50),
                result.get("scam_type", "unknown"),
                result.get("reasoning", "No reasoning provided"),
            )
        except Exception as e:
            print("Error in scam detection: " + str(e))
            return 50, "unknown", "Error in detection"


def load_grandma_persona():
    """Load the Grandma Gertrude persona from YAML file."""
    persona_path = os.path.join(
        os.path.dirname(__file__), "prompts", "grandma_persona.yaml"
    )

    with open(persona_path, "r", encoding="utf-8") as file:
        persona_data = yaml.safe_load(file)

    # Build comprehensive instructions from the YAML data
    instructions = f"""
    CRITICAL: NEVER include stage directions, tone descriptions, or non-verbal actions like "(in a sweet tone)", "*chuckles*", "(confused)", "pauses" etc.
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
    def __init__(self, llm) -> None:
        grandma_instructions = load_grandma_persona()
        super().__init__(instructions=grandma_instructions)
        self.scam_detector = ScamDetector(llm)
        self.scam_confidence = 0
        self.scam_type = "unknown"


async def entrypoint(ctx: agents.JobContext):
    # Initialize LLM with Cerebras
    llm = openai.LLM.with_cerebras(
        model="llama3.1-8b",
    )

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=llm,
        tts=cartesia.TTS(model="sonic-2", voice="d7e54830-4754-4b17-952c-bcdb7e80a2fb"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    assistant = Assistant(llm=llm)

    await session.start(
        room=ctx.room,
        agent=assistant,
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Listen for user messages and check for scams
    @session.on("user_speech_committed")
    async def _on_user_speech_committed(message: agents.llm.ChatMessage):
        if assistant.scam_detector:
            # Get scam confidence score using Cerebras speed
            confidence, scam_type, reasoning = (
                await assistant.scam_detector.detect_scam_confidence(message.content)
            )
            assistant.scam_confidence = confidence
            assistant.scam_type = scam_type

            # Print scam detection results for demo
            print(f"⚡ CEREBRAS ANALYSIS COMPLETE:")
            print(f'  📞 Message: "{message.content[:50]}..."')
            print(f"  📊 Confidence: {confidence}%")
            print(f"  🏷️ Type: {scam_type}")
            print(f"  💭 Reasoning: {reasoning}")

            # Escalate Grandma's tactics based on confidence
            if confidence > 75:
                print(f"🚨 HIGH CONFIDENCE SCAM DETECTED!")
                print(f"🎭 Grandma activating MAXIMUM time-wasting tactics!")
                # Could inject additional instructions here for high-confidence scams
            elif confidence > 50:
                print(f"⚠️ POTENTIAL SCAM DETECTED!")
                print(f"🎭 Grandma engaging enhanced confusion tactics!")
            else:
                print(f"✅ LIKELY LEGITIMATE CALL")
                print(f"🎭 Grandma using normal sweet elderly behavior")

            print(f"⏱️ Analysis completed in real-time using Cerebras speed!")
            print("-" * 60)

    await session.generate_reply(
        instructions=(
            "Greet the caller in character as Grandma Gertrude. "
            "Be sweet but slightly confused about who's calling and start talking about your benched 330 lbs."
        )
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
            # agent_name is required for explicit dispatch
            agent_name="my-telephony-agent",
        )
    )
