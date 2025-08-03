#!/usr/bin/env python3
"""Test script to verify YAML loading works correctly."""

import yaml
import os


def load_grandma_persona():
    """Load the Grandma Gertrude persona from YAML file."""
    persona_path = os.path.join(os.path.dirname(__file__), "prompts", "grandma_persona.yaml")

    with open(persona_path, 'r', encoding='utf-8') as file:
        persona_data = yaml.safe_load(file)

    # Build comprehensive instructions from the YAML data
    instructions = f"""
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
"""

    return instructions


if __name__ == "__main__":
    try:
        instructions = load_grandma_persona()
        print("✅ Successfully loaded Grandma persona!")
        print(f"📏 Instructions length: {len(instructions)} characters")
        print("\n🎭 Character loaded:")
        print("=" * 50)
        print(instructions[:500] + "..." if len(instructions) > 500 else instructions)
        print("=" * 50)
    except Exception as e:
        print(f"❌ Error loading persona: {e}")
