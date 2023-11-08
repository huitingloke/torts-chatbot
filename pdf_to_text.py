from pypdf import PdfReader
import os

def folder_pdf_to_text(folder_path):
    try:
        final_list = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                with open(os.path.join(folder_path, filename), "rb") as f: # must be read as rb for some reason idk it says on stack overflow HAHAHHA help
                    reader = PdfReader(f)
                    number_of_pages = len(reader.pages)
                    text_congealed = [reader.pages[i].extract_text() for i in range(number_of_pages)]
            final_list.append(text_congealed)

    except:
        print("Something went wrong with the PDF generation!")
        return False
    else:
        return final_list

