import csv
import os
import time
from docling.document_converter import DocumentConverter

input_folder = r"C:\Users\vundyalav\cuad_data\cuad\CUAD_v1\full_contract_pdf\Sample"
output_folder = r"C:\Users\vundyalav\cuad-pipeline\outputs\docling"
timing_csv = r"C:\Users\vundyalav\cuad-pipeline\outputs\timing_docling.csv"

os.makedirs(output_folder, exist_ok=True)

# Build the converter once. Docling loads its layout/table models lazily,
# so the first document's time includes model loading (warm-up).
converter = DocumentConverter()

results = []

for filename in sorted(os.listdir(input_folder)):
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(input_folder, filename)
    out_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".md")

    try:
        # Timer covers conversion and export to markdown (not writing the file)
        start_time = time.perf_counter()
        result = converter.convert(pdf_path)
        # Form feed (0x0C) separates pages, same as the PyMuPDF script
        text = result.document.export_to_markdown(page_break_placeholder="\x0c")
        elapsed_time = time.perf_counter() - start_time

        page_count = len(result.document.pages)

        with open(out_path, "w", encoding="utf-8") as output:
            output.write(text)

        results.append([filename, page_count, round(elapsed_time, 3), len(text), ""])
        print(f"Processed: {filename} | Pages: {page_count} | Time Taken: {elapsed_time:.2f} seconds")

    except Exception as e:
        results.append([filename, "", "", "", str(e)])
        print(f"FAILED: {filename} | {e}")

with open(timing_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "pages", "seconds", "chars", "error"])
    writer.writerows(results)

print("Done processing all PDFs!")
