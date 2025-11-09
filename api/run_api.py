from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from request_models import GenerateRequest
from openai import OpenAI
import os

load_dotenv()

app = FastAPI()

llm_client = OpenAI(
    base_url=os.environ.get('OPENAI_BASE_URL'), 
    api_key='empty'
)

@app.post('/generate', summary='Generate text')
async def generate(request: GenerateRequest):
    
    response = llm_client.responses.create(
        model=request.model_id,
        input=request.prompt,
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature
    ) 

    return response.output_text

@app.get('/list-models', summary='Lists available models')
async def list_models():

    models_info = llm_client.models.list() 
    model_ids = [model_info.id for model_info in models_info]
    
    return model_ids 

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': f'Failed with exception: {exc}'}
    )
