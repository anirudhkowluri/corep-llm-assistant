1.LLM-Assisted PRA COREP Reporting Assistant (Prototype)
📌 Overview

UK banks regulated by the Prudential Regulation Authority (PRA) must submit COREP regulatory returns that accurately reflect their capital position and prudential metrics. Preparing these returns is complex and error-prone because analysts must manually interpret dense regulatory rules and map them to structured COREP templates.

This project implements a prototype LLM-assisted regulatory reporting assistant that demonstrates end-to-end COREP reporting support for a constrained subset of COREP, focused on Own Funds (COREP C 01.00).

The system combines retrieval-augmented generation (RAG) with structured output, basic validation, and auditability, aligning with real-world regulatory expectations.

2.Objective

The goal of this prototype is to demonstrate how an LLM can:

Accept a natural-language regulatory question

Interpret a simple reporting scenario

Retrieve relevant PRA Rulebook and COREP instructions

Generate structured COREP-aligned output

Populate a human-readable COREP template extract

Flag missing or inconsistent data

Provide a rule-level audit trail

This is a proof-of-concept tool intended for decision support, not automated regulatory submission.

3.Scope (Intentionally Limited)

Reporting framework: COREP

Template covered:

C 01.00 – Own Funds

Regulatory sources:

PRA Rulebook (CRR Own Funds sections – sample extracts)

EBA COREP Instructions for C 01.00 (sample extracts)

The limited scope ensures the prototype is:

Realistic

Auditable

Easy to demonstrate end-to-end

4.Architecture
User Question + Scenario
        ↓
Regulatory Text Retrieval (RAG)
        ↓
LLM Structured JSON Output
        ↓
COREP Template Mapping
        ↓
Validation Rules
        ↓
COREP Extract + Audit Log

5. project structure
   corep_llm_assistant/
│
├── data/
│   ├── pra_rulebook.txt          # Sample PRA rule excerpts
│   └── corep_instructions.txt   # Sample COREP instructions
│
├── schemas/
│   └── c01_schema.json           # COREP C 01.00 schema
│
├── retrieval/
│   ├── ingest.py                # Builds vector index of regulatory texts
│   └── retriever.py             # Semantic search over rules
│
├── llm/
│   └── corep_generator.py       # Gemini LLM structured output generator
│
├── validation/
│   └── rules.py                 # Basic COREP validation checks
│
├── ui/
│   └── app.py                   # Streamlit UI
│
├── requirements.txt
└── README.md
5.Key Concepts Used
🔹 Retrieval-Augmented Generation (RAG)

Regulatory texts are embedded and indexed using FAISS

Only relevant rule paragraphs are provided to the LLM

Reduces hallucination and improves traceability

🔹 Structured Output

LLM output is constrained to valid JSON

Matches a predefined COREP schema

Every populated field includes a rule reference

🔹 Auditability

Each COREP field records:

Source regulation

Article / paragraph reference

Supports explainability for internal and regulatory review

🛠️ Technology Stack
| Component      | Technology             |
| -------------- | ---------------------- |
| LLM            | Gemini 1.5             |
| Embeddings     | Gemini embedding model |
| Vector store   | FAISS                  |
| Backend        | Python                 |
| UI             | Streamlit              |
| Validation     | Python rule checks     |
| Env management | python-dotenv          |

# steps to run the file
1️⃣ Clone the repository
git clone https://github.com/your-username/corep-llm-assistant.git
cd corep-llm-assistant

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # macOS/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up API key

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key_here


⚠️ Do not commit this file to GitHub.

5️⃣ Build regulatory vector index
python retrieval/ingest.py

6️⃣ Run the application
streamlit run ui/app.py

🧪 Example Inputs (For Demo)
Regulatory Question
How should CET1 capital be reported in COREP C 01.00 for a UK bank?

Reporting Scenario
UK incorporated bank.
Reporting template: COREP C 01.00 (Own Funds).
Retained earnings: 120 million GBP.
No Additional Tier 1 instruments.
No Tier 2 instruments.
