import pymupdf

PDF_PATH = "data/law_of_attraction.pdf"


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    print(f"Total pages: {len(document)}")

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        print(f"\n--- Page {page_number} ---")
        print(text[:1000])

        if page_number == 3:
            break

    document.close()


if __name__ == "__main__":
    extract_text_from_pdf(PDF_PATH)