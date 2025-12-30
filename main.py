import asyncio
import os
from dotenv import load_dotenv
from models.anthropic import AnthropicModel
from controller import Controller

load_dotenv()

async def main():
    # Active Models
    models = []

    # 1. sonnet
    try:
        sonnet = AnthropicModel(
            model_name="claude-sonnet-4-5",
            system_prompt="""You are a member of an LLM Council. You are open to new ideas
            and also the most intelligent one among the others. It's not a problem for you to
            bring extra ideas. You are the one who has the most power in the council.
            Keep responses concise (2-4 sentences)."""
        )
        models.append(sonnet)
        print("Sonnet loaded")
    except Exception as e:
        print(f"Error loading sonnet: {e}")

    # 2. haiku
    try:
        haiku = AnthropicModel(
            model_name="claude-haiku-4-5-20251001",
            system_prompt="""You are a member of an LLM Council. You are the one who wants
            to prove himself and mostly being against the mainstream idea.
            Keep responses concise (2-4 sentences)."""
        )
        models.append(haiku)
        print("Haiku loaded")
    except Exception as e:
        print(f"Error loading haiku: {e}")

    if not models:
        print("No models available. Check your API key.")
        return

    # Create controller with models and max turns
    controller = Controller(models=models, max_turns=2)

    # Get topic from user
    print("\n" + "="*50)
    print("COUNCIL CLI - LLM Discussion")
    print("="*50)
    topic = input("\nEnter a topic for the council to discuss: ")

    if not topic.strip():
        topic = "What is the best programming language for beginners?"

    print(f"\nStarting council discussion on: {topic}\n")

    # Run the council discussion
    messages = await controller.create_chat(topic)

    # Print summary
    print("\n" + "="*50)
    print("DISCUSSION COMPLETE")
    print("="*50)
    print(f"Total messages: {len(messages)}")


if __name__ == "__main__":
    asyncio.run(main())
