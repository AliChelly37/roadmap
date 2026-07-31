import fitz  # PyMuPDF

PDF_FILE = "document_test.pdf"

def parse_and_inspect_pdf(filepath):
    print(f"Ouverture du fichier PDF : '{filepath}'...")
    
    # S4-J1-T3 : Ingestion et ouverture avec PyMuPDF
    doc = fitz.open(filepath)
    
    print(f"Le document contient {len(doc)} pages.")
    
    # Extraction et inspection page par page
    for page_idx in range(len(doc)):
        page = doc.load_page(page_idx) # Charge la page
        text = page.get_text()         # Extrait le texte natif
        
        print(f"\n================ PAGE {page_idx + 1} (Index {page_idx}) ================")
        print(f"Metadata : {{'source': '{filepath}', 'page_number': {page_idx + 1}}}")
        print("----------------------------------------------------------------")
        print(text.strip())
        print("================================================================\n")

if __name__ == "__main__":
    parse_and_inspect_pdf(PDF_FILE)
