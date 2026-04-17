from fpdf import FPDF

def generate_study_notes(student_name: str, chat_history: list) -> bytes:
    """
    Converts a chat history into a downloadable PDF format.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", style='B', size=16)
    title = f"Study Notes for {student_name}"
    pdf.cell(200, 10, txt=title.encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')
    pdf.ln(10)
    
    # Chat Content
    for msg in chat_history:
        role = "Student" if msg["role"] == "user" else "AI Teacher"
        
        # FPDF default Arial only reliably supports latin-1. 
        # We replace unencodable characters (like emojis/hindi) with '?' to prevent crashing.
        safe_content = str(msg["content"]).encode('latin-1', 'replace').decode('latin-1')
        
        # Print Role Header
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=f"{role}:", ln=1)
        
        # Print Message Content
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, txt=safe_content)
        pdf.ln(5)
        
    # Output to byte string for Streamlit download button
    return bytes(pdf.output(dest='S'), 'latin-1')
