# Novatech Policy RAG API

Novatech Policy RAG API is a Retrieval-Augmented Generation (RAG) application built to make it easier to find information across company policy and internal knowledge documents.

Instead of manually searching through multiple documents, users can ask questions in natural language and receive relevant, context-aware answers. The application retrieves information from the available policy documents and uses the Groq LLM to generate the final response.

The backend is built with FastAPI, providing REST API endpoints and interactive Swagger documentation for testing the application.

## Key Features

- Ask natural-language questions about company policies
- Retrieve relevant information from multiple internal documents
- Generate context-aware responses using Groq
- Semantic document search using vector embeddings
- FastAPI-based REST API
- Interactive API testing through Swagger UI
- Secure API key management using environment variables

## Tech Stack

- Python
- FastAPI
- Groq
- Retrieval-Augmented Generation (RAG)
- ChromaDB
- Sentence Transformers
- Uvicorn

## Project Structure

```text
Novatech-Policy-RAG-API/
├── app/
│   └── main.py
├── data/
│   ├── company_hr_policy.txt
│   ├── engineering_standards.txt
│   ├── onboarding_guide.txt
│   ├── product_knowledge_base.txt
│   └── security_policy.txt
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md
```

## Running the Project Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd Novatech-Policy-RAG-API
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key
```

The `.env` file is excluded from Git and should never be committed to the repository.

### 5. Start the FastAPI application

```bash
uvicorn app.main:app --reload
```

### 6. Test the API

Once the application is running, open the FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

You can use the Swagger interface to test the available endpoints and submit questions to the RAG application.

## Security

Sensitive information such as the Groq API key is managed through environment variables. The `.env` file is excluded from version control through `.gitignore`, preventing credentials from being committed to the repository.

## Future Improvements

- Deploy the API to a public cloud environment
- Add a user-friendly web interface
- Improve document retrieval and ranking
- Add support for additional document formats
- Add authentication and API access controls
- Add automated testing and monitoring
