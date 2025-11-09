# Domain generator

This is a demo repository that contains various tools and experiments for web domain generation based on business descriptions.

The entrypoint to this repo is [docker-compose.yml](docker-compose.yml), which launches the following services:
- vllm - LLM inference framework, hosts both base and finetuned LLMs
- [api](api) - defines FastAPI routes to interact with LLMs hosted via `vllm` 

Configure via [.env](.env) file.

### Jupyter notebooks
[notebooks](notebooks) directory contain two .ipynb notebooks:
- [dataset_creation.ipynb](notebooks/dataset_creation.ipynb) - used to produce [dataset.jsonl](notebooks/dataset.jsonl) dataset for finetuning
- [domain_generation.ipynb](notebooks/domain_generation.ipynb) - showcases actual domain generation using various prompts and models

Notebooks are not containerized. I listed required packages inside notebooks themselves.

### Model finetuning
[training](training) directory contains [run_sft.py](training/run_sft.py) script that finetunes LoRA adapter for the base model `llama 3.1 8b` on custom dataset. Model adapter weights are saved in [training/finetuned_model](training/finetuned_model) directory.

## Build
Use docker compose to build the application:

`docker compose build`

## Run
Use docker compose to launch the application:

`docker compose up`

Note: it can take a while for vllm to initialize

## Next steps / further ideas
Here are a few ideas to improve on in the creation of domain names or to make this service more practical and production-ready:
- Connect with domain name lookup to see if generated domain is available
    - if unavailalbe, offer similar alternatives
- have a vector database with vectors of various business descriptions. When generating a new domain, use this vector database to find similar businesses and their domain names. These domains can be incorporated into a fewshot prompt to serve as examples.
- Make creation more intricate, generate in multiple steps: try to extract some categories about from the business description using an LLM: is business small/big, local/international, for-profit/non-profit, practical/premium. This information can be used to generate final domain.
- Include custom naming logic, ie: domain has to include an adverb, adjective, etc.
- Have a scorer / evaluator of domain names: is domain name catchy? does it have a lot of competition? is it unique? how well would it rank?
- Set up a price range and connect with domain provider services: domain generator will be able to generate more expensive domains (shorter, popular extension) or cheaper ones (longer, less popular extension).
    - ability to pre-select domain extension
- Control creativity of the generated domain (something like temperature) - closer to 0 would generate domains closer to literal business descriptions, ie: autoparts.com, while closer to 1 would generate domains that are creative but might not be reflective of the business, ie: wearebraindead.com for a clothing company
