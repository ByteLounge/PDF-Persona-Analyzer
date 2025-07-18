from sentence_transformers import SentenceTransformer, util
import fitz, json, os, time

model = SentenceTransformer("./all-MiniLM-L6-v2")

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if text.strip():
            sections.append((page_num, text))
    return sections

def rank_sections(persona, job, pdf_files, top_k=10):
    query = f"{persona}. {job}"
    query_emb = model.encode(query, convert_to_tensor=True)
    results = []
    for pdf in pdf_files:
        sections = extract_sections(pdf)
        for page_num, text in sections:
            section_emb = model.encode(text, convert_to_tensor=True)
            score = util.cos_sim(query_emb, section_emb).item()
            results.append({
                "document": os.path.basename(pdf),
                "page": page_num,
                "section_title": text.strip().split("\n")[0][:60],
                "importance_rank": round(score, 4)
            })
    results = sorted(results, key=lambda x: x["importance_rank"], reverse=True)[:top_k]
    return results

def refine_subsections(results, pdf_files, persona, job, top_sentences=3):
    query = f"{persona}. {job}"
    query_emb = model.encode(query, convert_to_tensor=True)
    refined = []
    for res in results:
        pdf_path = [p for p in pdf_files if os.path.basename(p) == res["document"]][0]
        doc = fitz.open(pdf_path)
        page_text = doc[res["page"] - 1].get_text()
        sentences = [s.strip() for s in page_text.split(".") if s.strip()]
        scored_sentences = []
        for s in sentences:
            s_emb = model.encode(s, convert_to_tensor=True)
            score = util.cos_sim(query_emb, s_emb).item()
            scored_sentences.append((score, s))
        top = sorted(scored_sentences, reverse=True)[:top_sentences]
        refined_text = ". ".join([s for _, s in top])
        refined.append({
            "document": res["document"],
            "page": res["page"],
            "refined_text": refined_text
        })
    return refined

if __name__ == "__main__":
    persona = os.getenv("PERSONA", "PhD Researcher in Computational Biology")
    job = os.getenv("JOB", "Prepare a literature review focusing on methodologies, datasets, and performance benchmarks")
    input_dir, output_dir = "/app/input", "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".pdf")]
    ranked_sections = rank_sections(persona, job, pdf_files)
    refined_texts = refine_subsections(ranked_sections, pdf_files, persona, job)
    output = {
        "metadata": {
            "input_documents": [os.path.basename(f) for f in pdf_files],
            "persona": persona,
            "job": job,
            "timestamp": time.ctime()
        },
        "sections": ranked_sections,
        "subsections": refined_texts
    }
    with open(os.path.join(output_dir, "persona_output.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print("✅ Round 1B completed: persona_output.json generated in /app/output")
