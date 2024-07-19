project_files = [
    "src/borrowing_ledger/__init__.py",
    "src/borrowing_ledger/components/__init__.py",
    "src/borrowing_ledger/components/speech_recognition.py",
    "src/borrowing_ledger/components/nlp_processor.py",
    "src/borrowing_ledger/components/query_generator.py",
    "src/borrowing_ledger/components/data_sync.py",
    "src/borrowing_ledger/pipelines/__init__.py",
    "src/borrowing_ledger/pipelines/input_processing_pipeline.py",
    "src/borrowing_ledger/pipelines/ledger_operation_pipeline.py",
    "src/borrowing_ledger/database/__init__.py",
    "src/borrowing_ledger/database/models.py",
    "src/borrowing_ledger/database/crud.py",
    "src/borrowing_ledger/api/__init__.py",
    "src/borrowing_ledger/api/routes.py",
    "src/borrowing_ledger/utils/__init__.py",
    "src/borrowing_ledger/utils/exception_handler.py",
    "src/borrowing_ledger/utils/logger.py",
    "src/borrowing_ledger/utils/helpers.py",
    "src/borrowing_ledger/config.py",
    "src/borrowing_ledger/main.py",
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

# Create the files
import os

for file_path in project_files:
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'w') as f:
        pass  # Create an empty file

print("Project structure created successfully!")
