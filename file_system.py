import os
from pathlib import Path
import logging
from src.borrowing_ledger.utils.logger import logger

logging.basicConfig(level=logging.INFO)
project_name="borrowing_ledger"

list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/speech_recognition.py",
    f"src/{project_name}/components/nlp_processor.py",
    f"src/{project_name}/components/query_generator.py",
    f"src/{project_name}/components/data_sync.py",
    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/pipelines/input_processing_pipeline.py",
    f"src/{project_name}/pipelines/ledger_operation_pipeline.py",
    f"src/{project_name}/database/__init__.py",
    f"src/{project_name}/database/models.py",
    f"src/{project_name}/database/crud.py",
    f"src/{project_name}/api/__init__.py",
    f"src/{project_name}/api/routes.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/exception_handler.py",
    f"src/{project_name}/utils/logger.py",
    f"src/{project_name}/utils/helpers.py",
    f"src/{project_name}/config.py",
    f"src/{project_name}/main.py",
    "tests/__init__.py",
    "tests/test_speech_recognition.py",
    "tests/test_nlp_processor.py",
    "tests/test_query_generator.py",
    "tests/test_data_sync.py",
    "Dockerfile",
    "requirements.txt",
    "README.md",
    ".gitignore"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename=os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logger.info(f"Creating directory: {filedir} for the file {filename}" )

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, 'w') as f:
            pass
        logger.info(f"Creating empty file: {filepath}")

    else:
        logger.info(f" {filename} is already exists")

