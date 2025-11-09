from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str
    model_id: str
    max_output_tokens: int = 256
    temperature: float = 0.7