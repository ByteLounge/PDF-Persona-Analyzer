## Approach Explanation

### Round 1A – Outline Extraction
- Extracts title and headings (H1, H2, H3) using PyMuPDF (font-size based clustering).
- Largest font in first pages = Title, subsequent distinct sizes = H1, H2, H3.
- Filters out paragraphs by word count.
- Runs under 10 seconds for 50 pages.

### Round 1B – Persona Intelligence
- Uses MiniLM (20MB, offline) to convert persona+job into query embedding.
- Computes cosine similarity with section/page embeddings, ranks top 10.
- Refines subsections by extracting top sentences.

### Constraints
- CPU-only, offline, <1GB model size, <60s for 3–5 PDFs.
