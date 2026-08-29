# 📚 Traditional RAG V1 — Document Question Answering

> A from-scratch **Retrieval-Augmented Generation (RAG)** pipeline for answering questions from domain-specific PDF documents.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![RAG](https://img.shields.io/badge/AI-Traditional%20RAG-purple)
![Embeddings](https://img.shields.io/badge/Embeddings-BGE--small-orange)
![Vector%20Search](https://img.shields.io/badge/Vector%20Search-FAISS-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 🎯 Project Overview

Large Language Models can generate fluent answers, but they do not automatically have access to a user's private or domain-specific documents.

This project implements a **Traditional RAG pipeline** that retrieves relevant information from a PDF and uses that retrieved context to support answer generation.

The project is being built **from the fundamentals upward**, with each stage implemented and inspected separately rather than hiding the entire workflow behind a high-level RAG library.

---

## 🧠 What is RAG?

RAG stands for **Retrieval-Augmented Generation**.

Instead of asking an LLM to answer a question entirely from its internal knowledge:

```text
User Question
      ↓
Retrieve relevant document information
      ↓
Provide retrieved context to LLM
      ↓
Generate grounded answer
```

This helps an application answer questions using information contained in a specific knowledge source.

---

# 🏗️ Architecture

```text
                    DOCUMENT INGESTION
                           │
                           ▼
                       PDF File
                           │
                           ▼
                       PyMuPDF
                           │
                           ▼
                    Text Extraction
                           │
                           ▼
                     Data Cleaning
                           │
                           ▼
                        Chunking
                           │
                           ▼
                 BGE-small Embeddings
                           │
                           ▼
                     Vector Index
                           │
                           ▼
                         FAISS
                           │
                           │
                    QUERY PIPELINE
                           │
                    User Question
                           │
                           ▼
                 BGE-small Embedding
                           │
                           ▼
                  Similarity Search
                           │
                           ▼
                    Top-K Chunks
                           │
                           ▼
                    ┌────────────┐
                    │    LLM     │
                    └────────────┘
                           │
                           ▼
                    Grounded Answer
```

---

# 🔨 Current Implementation

## 1. PDF Ingestion

The project uses **PyMuPDF** to open the PDF and extract text page by page.

Each page is represented with metadata:

```python
{
    "page_number": 1,
    "text": "..."
}
```

This preserves the relationship between extracted content and its source page.

---

## 2. Data Cleaning

The extracted text is cleaned conservatively.

Current preprocessing includes:

* Normalizing line endings
* Removing trailing whitespace
* Replacing tabs with spaces
* Reducing excessive blank lines
* Preserving headings and document structure
* Preserving the original meaning of the source

The principle is:

> **Clean formatting noise without modifying the document's meaning.**

---

## 3. Chunking

The cleaned text is divided into smaller retrieval units using LangChain's `RecursiveCharacterTextSplitter`.

Current V1 configuration:

```text
Chunk size:     800 characters
Chunk overlap:  150 characters
```

The current dataset produced:

```text
15 pages
↓
51 chunks
```

Chunk inspection was performed before embedding to verify that boundaries preserved meaningful context.

---

## 4. Embeddings

Each chunk is converted into a numerical representation using:

**`BAAI/bge-small-en-v1.5`**

The embedding model produces:

```text
384-dimensional vectors
```

For the current dataset:

```text
51 chunks
    ↓
BGE-small
    ↓
51 × 384-dimensional vectors
```

The embedding model is used for both document chunks and user queries so that they can be compared in the same vector space.

---

## 5. Vector Search with FAISS

The generated embeddings are indexed using:

```text
FAISS IndexFlatL2
```

The current V1 index contains:

```text
51 vectors
```

At query time:

```text
User Question
      ↓
BGE-small
      ↓
Query Vector
      ↓
FAISS
      ↓
Top-K Similar Chunks
```

For example, a query about the male reproductive system successfully retrieved a chunk containing the relevant section:

```text
2.1 THE MALE REPRODUCTIVE SYSTEM
```

This demonstrates that semantic retrieval is working before an LLM is introduced.

---

# 📊 Current Project Status

| Component               | Status  |
| ----------------------- | ------- |
| PDF selection           | ✅       |
| PDF ingestion           | ✅       |
| Text extraction         | ✅       |
| Extraction validation   | ✅       |
| Data cleaning           | ✅       |
| Chunking                | ✅       |
| Chunk inspection        | ✅       |
| BGE-small embeddings    | ✅       |
| FAISS indexing          | ✅       |
| Semantic retrieval      | ✅       |
| LLM generation          | 🚧 Next |
| End-to-end RAG          | 🚧      |
| Evaluation              | 🚧      |
| Persistent vector store | 🚧      |
| API / UI                | 🔜      |
| Agentic RAG             | 🔜 V2   |

---

# 🧰 Technology Stack

### Programming

* Python 3.12
* Jupyter Notebook

### Document Processing

* PyMuPDF

### RAG Framework

* LangChain
* LangChain Text Splitters

### Embeddings

* Sentence Transformers
* BAAI/bge-small-en-v1.5

### Vector Search

* FAISS

### Planned

* LLM API
* Persistent vector store
* Retrieval evaluation
* API/UI layer
* Agentic RAG

---

# 📁 Planned Project Structure

```text
traditional-rag-v1/
│
├── data/
│   └── reproduction.pdf       # local dataset, not committed
│
├── notebooks/
│   └── rag_v1_exploration.ipynb
│
├── src/
│   ├── ingest.py
│   ├── clean.py
│   ├── chunk.py
│   ├── embed.py
│   └── retrieve.py
│
├── vectorstore/
│   └── faiss_index/
│
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```


---

# 🎓 Learning Goals

This project is designed to understand what happens **behind the scenes of a RAG system**, including:

* Why LLMs need external knowledge
* Why documents are chunked
* How embeddings represent semantic meaning
* How vector similarity works
* Why FAISS is used
* How retrieval differs from generation
* How retrieved context is passed to an LLM
* How retrieval quality affects final answers
* How Traditional RAG can evolve into Agentic RAG

---

## 📌 Current Status

**Traditional RAG V1 is currently at the semantic retrieval stage.**

The next milestone is connecting retrieved document context to an LLM to complete the **Retrieval-Augmented Generation** loop.
