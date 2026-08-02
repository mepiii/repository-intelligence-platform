# System Architecture

The Repository Intelligence Platform is built around clean architecture principles and a layered pipeline.

## Layers

1. **Scanner Layer**: Extract metadata from Git repositories and manifest files.
2. **AST Intelligence Layer**: Parse AST tree representation to index symbols, docstrings, and imports.
3. **Semantic Embedding Layer**: Vectorize code fragments, docstrings, and commit messages with pgvector.
4. **Knowledge Graph Layer**: Synchronize graph structures in Neo4j.
5. **AI Assistant Layer**: Multi-source retriever (Graph + Semantic + Commits) supplying formatted context to LLM engines.
