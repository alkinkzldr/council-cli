import asyncio
from typing import List, Dict
#from display import DisplayManager
from datetime import datetime
import time

class Controller:
    
    def __init__(self, models:List, max_turns:int):
        self.models = models
        self.max_turns = max_turns
        self.prev_messages = []
        
    def add_message(self, content: str, model_name: str, role: str = "assistant"):
        """Add a message to conversation history"""
        self.prev_messages.append({
            "role": role,
            "content": content,
            "model": model_name,
            "timestamp": time.time()
        })

    async def create_chat(self, topic:str, system:str=None):
        start_time = time.time()

        # Add the initial topic as a user message
        self.prev_messages.append({
            "role": "user",
            "content": topic,
            "model": "user",
            "timestamp": start_time
        })

        # Conversation loop
        for turn in range(self.max_turns):
            print(f"\n{'#'*50}")
            print(f"# TURN {turn + 1} of {self.max_turns}")
            print(f"{'#'*50}")

            system_prompt = f"""This is a council meeting of different AI Models discussing a topic.
Other council members' messages are labeled with their name in brackets like [model-name].
You must respond directly to what others have said - agree, disagree, or build on their points.
This is turn {turn + 1} of {self.max_turns}.
Keep your response concise (2-4 sentences). Do not use markdown headers or formatting."""

            # Each model takes a turn
            for model in self.models:
                await self._model_turn(model, system_prompt)

        # Final conclusion round
        await self._conclusion_round()

        return self.prev_messages

    async def _conclusion_round(self):
        print(f"\n{'#'*50}")
        print(f"# FINAL CONCLUSION")
        print(f"{'#'*50}")

        conclusion_prompt = """This is the final round of the council meeting.
                    Other council members' messages are labeled with their name in brackets like [model-name].
                    Summarize what the council has agreed upon. State the consensus clearly in 2-3 sentences.
                    If there were disagreements, briefly note them. End with the council's final recommendation."""

        # Only first model gives conclusion to avoid repetition
        leader = self.models[0]
        await self._model_turn(leader, conclusion_prompt)

    async def _model_turn(self, model, system_prompt:str=None):
        # Build messages with speaker labels so models know who said what
        messages = []
        for msg in self.prev_messages:
            if msg["role"] == "user":
                messages.append({
                    "role": "user",
                    "content": msg["content"]
                })
            else:
                # Format assistant messages with the model name prefix
                speaker = msg.get("model", "unknown")
                if speaker == model.name:
                    # This model's own previous message
                    messages.append({
                        "role": "assistant",
                        "content": msg["content"]
                    })
                else:
                    # Another model's message - show as user message with label
                    messages.append({
                        "role": "user",
                        "content": f"[{speaker}]: {msg['content']}"
                    })
            
        try:
            # Get response from model
            response = await model.chat(messages, system_prompt)
        except Exception as e:
            print(f"\n[ERROR] {model.name} failed: {str(e)}")
            return
        
        self.add_message(
            content=response["content"],
            model_name=model.name
        )
        
        self._print_response(model.name, response["content"], response.get("tokens"))

    def _print_response(self, model_name: str, content: str, tokens: int = None):
        """Print model response to console"""
        print(f"\n{'='*50}")
        print(f"[{model_name}]")
        print(f"{'='*50}")
        print(content)
        if tokens:
            print(f"\n(tokens: {tokens})")