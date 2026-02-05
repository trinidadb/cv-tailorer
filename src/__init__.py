import os
from dotenv import load_dotenv

load_dotenv()

env_variables_names = ["GEMINI_API_KEY"]
for env_variable in env_variables_names:
    if env_variable not in os.environ:
        raise Exception(f"{env_variable} env variable should be defined")
