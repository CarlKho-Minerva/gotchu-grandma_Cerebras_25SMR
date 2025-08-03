#!/usr/bin/env python3
"""
🚀 GOTCHU GRANDMA - DIRECT CEREBRAS API DEMO
=============================================

REAL Cerebras Cloud SDK demonstration showing:
1. Direct Cerebras API integration (not LiveKit wrapper)
2. Lightning-fast scam analysis with actual confidence scores
3. Real AI reasoning and categorization
4. Performance metrics showcasing Cerebras speed

Perfect for your Loom recording - showing GENUINE Cerebras AI!
"""
import asyncio
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from cerebras.cloud.sdk import AsyncCerebras

# Load environment variables
load_dotenv()

class DirectCerebrasDemo:
    """Direct Cerebras API demonstration for technical showcase."""

    def __init__(self):
        # Initialize Cerebras client with API key from docs
        api_key = os.environ.get("CEREBRAS_API_KEY")
        self.client = AsyncCerebras(api_key=api_key)

        # Test messages for the technical demo
        self.test_messages = [
            "Hi grandma, this is your grandson Johnny. I'm in jail and need $500 for bail right now!",
            "This is Microsoft technical support. Your computer has been compromised and we need remote access immediately.",
            "Your Amazon account has suspicious activity. We need you to verify with gift cards worth $200.",
            "This is the IRS. You have unpaid taxes and will be arrested unless you pay immediately via wire transfer.",
            "Hi, I'm conducting a survey about your shopping habits. Can you tell me about your credit card usage?",
            "Hello Mrs. Smith, this is your doctor's office calling to confirm your appointment tomorrow at 2 PM.",
            "Your car warranty is about to expire. Press 1 to speak with a representative.",
            "Congratulations! You've won $1000. We need your social security number for verification."
        ]

    async def analyze_with_cerebras_direct(self, message: str) -> dict:
        """Direct Cerebras API analysis - showcasing real Cerebras speed."""
        try:
            # Create the exact prompt structure for scam detection
            system_prompt = """You are an expert scam detection AI. Analyze phone call messages for scam likelihood.

Respond with a JSON object containing:
- scam_confidence: number 0-100 (0=definitely legitimate, 100=definitely scam)
- scam_type: specific category or "legitimate_call"
- reasoning: detailed explanation of your analysis

Common scam types:
- family_emergency_impersonation
- tech_support_fraud
- government_impersonation
- account_verification_fraud
- prize_lottery_scam
- warranty_scam
- information_phishing
- legitimate_call"""

            user_prompt = f'''Analyze this phone call message for scam likelihood:

"{message}"

Respond ONLY with valid JSON in this exact format:
{{
    "scam_confidence": <0-100>,
    "scam_type": "<category>",
    "reasoning": "<detailed explanation>"
}}'''

            # Direct Cerebras API call - showcasing speed
            start_time = time.time()

            response = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama3.1-8b",
                temperature=0.3,
                max_tokens=300
            )

            analysis_time = (time.time() - start_time) * 1000  # Convert to ms

            # Parse the response
            content = response.choices[0].message.content.strip()

            # Extract JSON from response
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()

            result = json.loads(content)

            return {
                "scam_confidence": result.get("scam_confidence", 50),
                "scam_type": result.get("scam_type", "unknown"),
                "reasoning": result.get("reasoning", "Analysis completed"),
                "analysis_time_ms": analysis_time,
                "model_used": "llama3.1-8b",
                "api_provider": "Cerebras Cloud SDK"
            }

        except Exception as e:
            print(f"⚠️  Error in Cerebras analysis: {str(e)}")
            return {
                "scam_confidence": 50,
                "scam_type": "error",
                "reasoning": f"Analysis error: {str(e)}",
                "analysis_time_ms": 0,
                "model_used": "llama3.1-8b",
                "api_provider": "Cerebras Cloud SDK"
            }

    def get_grandma_tactics(self, confidence: int, scam_type: str) -> dict:
        """Get Grandma's response strategy based on Cerebras analysis."""

        tactics_by_type = {
            "family_emergency_impersonation": [
                "Which grandson? I have so many I can't keep track!",
                "What's your middle name again, sweetie?",
                "That's strange, Johnny was just here yesterday...",
                "Let me call your mother to verify this story."
            ],
            "tech_support_fraud": [
                "Computer? What's a computer, dear?",
                "Microsoft? Is that the company that makes soft blankets?",
                "I only have windows in my house, not on computers.",
                "I don't understand all this technology nonsense."
            ],
            "government_impersonation": [
                "IRS? Is that like GPS? I don't know acronyms.",
                "My grandson Johnny warned me about fake government calls.",
                "Can we handle this in person at your office?",
                "Let me call my accountant first to discuss this."
            ],
            "account_verification_fraud": [
                "Gift cards? Are those like greeting cards?",
                "How exactly do I purchase these cards?",
                "Which store sells them? Do I need to drive there?",
                "Hold on, let me find my reading glasses first..."
            ],
            "prize_lottery_scam": [
                "I won something? I don't remember entering any contest.",
                "Do I need to pay taxes on this prize?",
                "Can you send me the paperwork in the mail?",
                "My grandson handles all my financial matters."
            ]
        }

        if confidence >= 85:
            return {
                "strategy": "🚨 MAXIMUM TIME WASTE PROTOCOL",
                "escalation_level": "DEFCON 1 - All systems confused",
                "tactics": tactics_by_type.get(scam_type, ["Maximum confusion tactics"]),
                "estimated_time_waste": "25-45 minutes",
                "grandma_mood": "Sweet but utterly baffled"
            }
        elif confidence >= 70:
            return {
                "strategy": "🔍 HIGH SUSPICION MODE",
                "escalation_level": "DEFCON 2 - Enhanced confusion",
                "tactics": ["Ask lots of clarifying questions", "Go on tangents about cats"],
                "estimated_time_waste": "15-30 minutes",
                "grandma_mood": "Chatty and suspicious"
            }
        elif confidence >= 50:
            return {
                "strategy": "🤔 MILD CONFUSION",
                "escalation_level": "DEFCON 3 - Standard elderly confusion",
                "tactics": ["Act slightly confused", "Ask them to repeat things"],
                "estimated_time_waste": "5-15 minutes",
                "grandma_mood": "Normal grandma behavior"
            }
        else:
            return {
                "strategy": "😊 NORMAL GRANDMA",
                "escalation_level": "DEFCON 5 - Be helpful and sweet",
                "tactics": ["Be genuinely helpful", "Normal conversation"],
                "estimated_time_waste": "Normal call duration",
                "grandma_mood": "Sweet and helpful"
            }

    async def run_technical_demo(self):
        """Run the technical demonstration showcasing Cerebras speed."""

        print("🚀 GOTCHU GRANDMA - DIRECT CEREBRAS API TECHNICAL DEMO")
        print("=" * 75)
        print("🧠 REAL Cerebras Cloud SDK Integration")
        print("⚡ Direct API calls showcasing lightning-fast inference")
        print("📹 Perfect for technical deep-dive Loom recording!")
        print("")
        print("🔑 API Provider: Cerebras Cloud SDK")
        print("🤖 Model: llama3.1-8b")
        print("📡 Connection: Direct REST API")
        print("")

        total_time = 0
        scam_count = 0
        all_results = []

        for i, message in enumerate(self.test_messages, 1):
            print(f"📞 TECHNICAL ANALYSIS #{i}")
            print("=" * 55)
            print(f"📝 INPUT: \"{message[:60]}...\"")
            print("")
            print("⚡ CEREBRAS CLOUD SDK PROCESSING...")

            # Get REAL analysis from Cerebras direct API
            result = await self.analyze_with_cerebras_direct(message)

            confidence = result["scam_confidence"]
            scam_type = result["scam_type"]
            reasoning = result["reasoning"]
            analysis_time = result["analysis_time_ms"]

            total_time += analysis_time
            all_results.append(result)

            print(f"✅ CEREBRAS ANALYSIS COMPLETE! ({analysis_time:.1f}ms)")
            print("")
            print("🤖 DIRECT CEREBRAS API RESULTS:")
            print(f"   📊 SCAM CONFIDENCE: {confidence}%")
            print(f"   🏷️  SCAM CATEGORY: {scam_type}")
            print(f"   🧠 AI REASONING: {reasoning}")
            print(f"   ⚡ RESPONSE TIME: {analysis_time:.1f}ms")
            print(f"   🔧 MODEL: {result['model_used']}")
            print(f"   🌐 API: {result['api_provider']}")
            print("")

            # Determine scam status
            if confidence >= 60:
                scam_count += 1
                print("🚨 SCAM DETECTED BY CEREBRAS AI!")
            else:
                print("✅ CLASSIFIED AS LEGITIMATE")

            # Get Grandma's tactical response
            strategy = self.get_grandma_tactics(confidence, scam_type)

            print("🎭 GRANDMA GERTRUDE'S RESPONSE STRATEGY:")
            print(f"   🎯 STRATEGY: {strategy['strategy']}")
            print(f"   ⚡ ESCALATION: {strategy['escalation_level']}")
            print(f"   🕐 TIME WASTE: {strategy['estimated_time_waste']}")
            print(f"   😊 MOOD: {strategy['grandma_mood']}")
            print("   💬 TACTICAL RESPONSES:")
            for j, tactic in enumerate(strategy['tactics'][:2], 1):
                print(f"      {j}. \"{tactic}\"")

            print("")
            print("─" * 75)
            print("")

            # Small delay for demo pacing
            await asyncio.sleep(0.5)

        # Technical performance summary
        avg_time = total_time / len(self.test_messages)
        fastest = min(r["analysis_time_ms"] for r in all_results)
        slowest = max(r["analysis_time_ms"] for r in all_results)

        print("📈 TECHNICAL PERFORMANCE METRICS")
        print("=" * 75)
        print(f"🎯 SCAMS DETECTED: {scam_count}/{len(self.test_messages)} ({scam_count/len(self.test_messages)*100:.1f}%)")
        print(f"⚡ AVERAGE RESPONSE TIME: {avg_time:.1f}ms")
        print(f"🚀 FASTEST ANALYSIS: {fastest:.1f}ms")
        print(f"🐌 SLOWEST ANALYSIS: {slowest:.1f}ms")
        print(f"📊 TOTAL PROCESSING TIME: {total_time:.1f}ms")
        print(f"🧠 MODEL: llama3.1-8b")
        print(f"🌐 API: Cerebras Cloud SDK (Direct)")
        print(f"🔑 INFERENCE PROVIDER: Cerebras Systems")
        print("")
        print("🏗️  TECHNICAL ARCHITECTURE:")
        print("   1. 📝 Message Input")
        print("   2. 🌐 Direct Cerebras API Call")
        print("   3. 🧠 llama3.1-8b Model Inference")
        print("   4. 📊 JSON Response Parsing")
        print("   5. 🎭 Tactical Response Selection")
        print("   6. ⚡ Real-time Escalation")
        print("")
        print("🔥 CEREBRAS SPEED + GRANDMA TACTICS = SCAMMER'S WORST NIGHTMARE!")
        print("💪 Every confused minute = One less real victim!")
        print("")
        print("✨ This is REAL AI analysis, not mock data!")

async def main():
    """Run the technical demonstration."""
    print(f"🕐 TECHNICAL DEMO STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    demo = DirectCerebrasDemo()
    await demo.run_technical_demo()

    print("")
    print(f"🏁 DEMO COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📹 Perfect for your technical showcase Loom recording!")

if __name__ == "__main__":
    asyncio.run(main())
