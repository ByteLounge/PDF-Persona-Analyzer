import fitz  # PyMuPDF
import json
import os

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = {}
    title = ""
    outline = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = round(span["size"], 1)
                    if not text or len(text) > 12:
                        continue
                    font_sizes.setdefault(size, []).append((text, page_num))

    sorted_sizes = sorted(font_sizes.keys(), reverse=True)
    if not sorted_sizes:
        return {"title": "", "outline": []}

    title_candidates = [t[0] for t in font_sizes[sorted_sizes[0]] if t[1] <= 2]
    title = title_candidates[0] if title_candidates else font_sizes[sorted_sizes[0]][0][0]

    level_map = {sorted_sizes[0]: "Title"}
    for i, size in enumerate(sorted_sizes[1:4], start=1):
        level_map[size] = f"H{i}"

    for size, entries in font_sizes.items():
        level = level_map.get(size, None)
        if level and level != "Title":
            for text, page_num in entries:
                outline.append({"level": level, "text": text, "page": page_num})

    return {"title": title, "outline": outline}

if __name__ == "__main__":
    input_dir, output_dir = "/app/input", "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            result = extract_outline(os.path.join(input_dir, file))
            out_file = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
    print("✅ Round 1A completed: JSONs generated in /app/output")
