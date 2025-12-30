import os
import anthropic
from dotenv import load_dotenv
from typing import List, Dict

class BaseModel:
    
    def __init__(self, model_stamp:str=None):
        self.model_stamp = model_stamp
        
        