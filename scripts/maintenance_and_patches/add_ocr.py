import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\nlp_engine.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_strategy = """
    # Strategy 3: OCR Fallback for scanned/image-based PDFs
    try:
        import pdf2image
        import pytesseract
        import platform
        
        # Windows compatibility common paths
        if platform.system() == 'Windows':
            if os.path.exists(r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'):
                pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
                
        # Limit to first 3 pages to avoid timeout on massive image PDFs
        images = pdf2image.convert_from_bytes(pdf_bytes, dpi=200, first_page=1, last_page=3)
        ocr_text = []
        for img in images:
            text = pytesseract.image_to_string(img)
            if text and text.strip():
                ocr_text.append(text.strip())
                
        if ocr_text:
            combined_ocr = " ".join(ocr_text).strip()
            if len(combined_ocr) >= 50:
                return combined_ocr
    except Exception as e:
        print(f"[PDF Extraction Warning] OCR Fallback failed (Tesseract/Poppler likely not installed): {e}")

    return full_text if full_text else ""
"""

target = '    return full_text if full_text else ""'

if target in content:
    content = content.replace(target, new_strategy)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected OCR fallback into nlp_engine.py")
else:
    print("Could not find target string in nlp_engine.py")
