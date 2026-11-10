import csv
import os
import time
import pymupdf

# Define your folder paths (adjust these to your actual paths)
input_folder = r"C:\\Users\\vundyalav\\cuad_data\\cuad\\CUAD_v1\\full_contract_pdf\\Sample"
output_folder = r"C:\\Users\\vundyalav\\cuad-pipeline\\outputs\\pymupdf"
timing_csv = r"C:\\Users\\vundyalav\\cuad-pipeline\\outputs\\timing_pymupdf.csv"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

results = []

# Loop through all PDF files in the input folder, in a fixed order
for filename in sorted(os.listdir(input_folder)):
    # Process only PDF files
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(input_folder, filename)
    text_filename = os.path.splitext(filename)[0] + ".txt"
    txt_path = os.path.join(output_folder, text_filename)

    try:
        # Timer covers opening the PDF and extracting text only (not writing the file)
        start_time = time.perf_counter()
        with pymupdf.open(pdf_path) as doc:
            page_count = len(doc)
            # Form feed (0x0C) separates pages so text can be mapped back to pages later
            text = "\x0c".join(page.get_text() for page in doc)
        elapsed_time = time.perf_counter() - start_time

        with open(txt_path, "w", encoding="utf-8") as output:
            output.write(text)

        results.append([filename, page_count, round(elapsed_time, 3), len(text), ""])
        print(f"Processed: {filename} | Pages: {page_count} | Time Taken: {elapsed_time:.2f} seconds")

    except Exception as e:
        results.append([filename, "", "", "", str(e)])
        print(f"FAILED: {filename} | {e}")

# Save per-document stats so they can be compared with other parsers later
with open(timing_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "pages", "seconds", "chars", "error"])
    writer.writerows(results)

print("Done processing all PDFs!")
