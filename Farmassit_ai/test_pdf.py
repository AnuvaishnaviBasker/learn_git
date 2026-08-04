from pathlib import Path

from pypdf import PdfReader


pdf_folder = Path("data/pdfs")

for pdf_file in pdf_folder.glob("*.pdf"):
    print(f"\nReading: {pdf_file.name}")

    try:
        reader = PdfReader(str(pdf_file))

        print(f"Number of pages: {len(reader.pages)}")

        first_page_text = reader.pages[0].extract_text() or ""

        print("First-page preview:")
        print(first_page_text[:500])

    except Exception as error:
        print(f"Failed to read {pdf_file.name}: {error}")