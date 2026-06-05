# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Funathon (non-competitive hackathon) project focused on **automatic NACE classification** — mapping free-text activity descriptions to NACE 2.1 codes (European statistical classification of economic activities). The project explores two independent approaches:

1. **Supervised learning**: Deep learning text classifier using torchTextClassifiers
2. **RAG pipeline**: Retrieval-augmented generation combining vector database (Qdrant) with LLM

The project is built as a Quarto website with interactive tutorials deployed to GitHub Pages.

## Development Environment

### Python Environment Setup

```bash
# Install dependencies (creates .venv/ and installs from uv.lock)
uv sync

# Run Python scripts with the virtual environment
uv run python <script.py>

# Interactive development: point VS Code to .venv/bin/python
```

Python version: 3.13+

### Key Dependencies

- **ML/DL**: torch (CPU-only from pytorch.org), torchTextClassifiers, transformers, scikit-learn
- **Data**: pandas, polars, duckdb, numpy
- **MLOps**: mlflow (experiment tracking), qdrant-client (vector DB)
- **LLM**: openai (for LLM Lab API)
- **Publishing**: quarto (website generation)

### Environment Variables

Required in `.env` file (never commit this):

```
QDRANT_URL=https://...qdrant.user.lab.sspcloud.fr/
QDRANT_API_KEY=...
QDRANT_API_PORT=443
LLMLAB_API_KEY=...
LLMLAB_URL=https://llm.lab.sspcloud.fr/api
MLFLOW_TRACKING_URI=https://...mlflow.user.lab.sspcloud.fr/
MLFLOW_TRACKING_USERNAME=...
MLFLOW_TRACKING_PASSWORD=...
```

## Project Structure

```
.
├── index.qmd                    # Landing page
├── 1-ttc.qmd                    # Part 1: Supervised learning tutorial
├── 2-rag-intro.qmd              # Part 2: RAG introduction
├── 2-rag-vdb.qmd                # Part 2: Vector DB creation
├── 2-rag-generation.qmd         # Part 2: LLM generation
├── lk-ml.py                     # Standalone ML training script
├── solutions/                   # Reference solutions
├── _quarto.yaml                 # Quarto site configuration
├── pyproject.toml               # Python dependencies (uv format)
└── uv.lock                      # Locked dependency versions
```

## Common Commands

### Development

```bash
# Preview the Quarto website locally (auto-reload on changes)
uv run quarto preview

# Render the entire site to _site/
uv run quarto render

# Run a specific Python script
uv run python lk-ml.py

# Interactive cell-based development in VS Code
# Create a .py file with # %% cell markers and run cells with Shift+Enter
```

### Testing and CI

```bash
# Tests are defined in .github/workflows/tests.yaml
# Run locally with:
uv run quarto render --execute
```

### Publishing

The site auto-publishes to GitHub Pages on push to `main` via `.github/workflows/publish.yaml`.

## Architecture Notes

### Part 1: Supervised Learning (torchTextClassifiers)

- **Dataset**: Parquet file from S3 with `(label, code)` pairs
- **Pipeline**: 
  1. Load data with polars
  2. Train/val/test split (70/15/15)
  3. Encode labels with sklearn LabelEncoder
  4. Train WordPiece tokenizer (vocab_size=5000)
  5. Train classifier with torchTextClassifiers
  6. Log to MLflow for experiment tracking
- **Model**: Embedding-based text classifier (configurable embedding_dim, default 96)
- **Evaluation**: Top-k accuracy, Captum-based word attributions for explainability

### Part 2: RAG Pipeline

- **Vector DB**: Qdrant stores embedded NACE definitions
- **Retrieval**: Query Qdrant for top-k similar NACE codes given activity text
- **Generation**: Pass retrieved context + query to LLM (via LLM Lab API) for final classification
- **Evaluation**: Compare RAG predictions against ground truth

### Quarto Website

- **Format**: HTML with cosmo theme + custom.scss
- **Execution**: Code cells are cached (`cache: true`) to speed up renders
- **Navigation**: Navbar with links to all tutorial pages
- **Deployment**: GitHub Actions renders and publishes to gh-pages branch

## Development Patterns

### Interactive Exploration

Create scratch files at the repo root with cell markers:

```python
# %%
import pandas as pd

df = pd.read_parquet("https://minio.lab.sspcloud.fr/...")
df.head()

# %%
# Next cell
```

Run cells individually with Shift+Enter in VS Code.

### MLflow Experiment Tracking

```python
mlflow.set_experiment("funathon-2026-project2")
mlflow.pytorch.autolog()

with mlflow.start_run() as run:
    ttc.train(X_train, y_train, ...)
    mlflow.log_artifacts(training_config.save_path, artifact_path="model_artifacts")
```

### Loading Pretrained Models

Models are stored in S3 and loaded via s3fs:

```python
fs = s3fs.S3FileSystem(anon=True, endpoint_url="https://minio.lab.sspcloud.fr")
fs.get("projet-funathon/diffusion/mlflow-artifacts/", "./mlflow-artifacts/", recursive=True)
ttc = torchTextClassifiers.load("./mlflow-artifacts/")
```

## Important Notes

- **PyTorch**: Uses CPU-only wheels from pytorch.org (configured in `pyproject.toml`)
- **torchTextClassifiers**: Installed from GitHub (InseeFrLab/torchTextClassifiers)
- **Data source**: All datasets are public on SSPCloud S3 (minio.lab.sspcloud.fr)
- **Secrets**: Never commit `.env` — it's in `.gitignore`
- **Quarto caching**: Cached outputs in `_freeze/` speed up renders but may need clearing if code changes

## Target Audience

The tutorials are designed for three levels:
- **Beginner**: Follow along and understand provided solutions
- **Intermediate**: Complete exercises without checking answers
- **Expert**: Enhance the pipeline (better models, prompt tuning, richer embeddings)
