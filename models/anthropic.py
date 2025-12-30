import os
import anthropic
from dotenv import load_dotenv
from typing import List, Dict
from models.base_model import BaseModel

load_dotenv()

class AnthropicModel(BaseModel):

    def __init__(self, model_name: str, system_prompt: str = "", max_tokens: int = 1024):
        super().__init__(model_stamp="Anthropic")
        self.model = model_name
        self.name = model_name
        self.key = os.getenv("ANTHROPIC_API_KEY")
        self.instruction = system_prompt
        self.max_tokens = max_tokens
        self.client = anthropic.Anthropic(api_key=self.key)

    
    def add_instruction(self, message:str):
        self.instruction = message
        
    def add_max_tokens(self, tokens:int):
        self.max_tokens = tokens
    
    def interact(self, messages: List[Dict]) -> Dict:
        system_prompt = self.instruction
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=messages
        )

        # Extract text from content blocks
        text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                text += block.text

        return {
            "content": text,
            "role": response.role,
            "tokens": response.usage.output_tokens
        }

    async def chat(self, messages: List[Dict], system_prompt: str = None) -> Dict:
        """Async wrapper for interact method"""
        if system_prompt:
            original_instruction = self.instruction
            self.instruction = system_prompt + "\n\n" + self.instruction

        result = self.interact(messages)

        if system_prompt:
            self.instruction = original_instruction

        return result
            
        

