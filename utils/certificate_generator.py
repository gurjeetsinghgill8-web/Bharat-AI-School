import io
from fpdf import FPDF
from datetime import datetime

def generate_certificate(username: str, project_name: str) -> bytes:
    """
    Generates a professional Certificate of Completion using FPDF.
    Returns the PDF as bytes for Streamlit downloading.
    """
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    
    # Border
    pdf.set_line_width(2)
    pdf.rect(10, 10, 277, 190)
    
    # Title
    pdf.set_font("Arial", "B", 34)
    pdf.set_text_color(20, 50, 100)
    pdf.cell(0, 40, "CERTIFICATE OF COMPLETION", ln=True, align="C")
    
    # Subtitle
    pdf.set_font("Arial", "I", 16)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 20, "This proudly certifies that", ln=True, align="C")
    
    # Username
    pdf.set_font("Arial", "B", 28)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 30, username.upper(), ln=True, align="C")
    
    # Description
    pdf.set_font("Arial", "", 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "has successfully built and deployed the AI project:", ln=True, align="C")
    
    # Project Name
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(20, 100, 50)
    pdf.cell(0, 20, project_name, ln=True, align="C")
    
    # Footer
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    date_str = datetime.now().strftime("%B %d, %Y")
    
    pdf.set_y(150)
    pdf.cell(100, 10, f"Date: {date_str}", ln=False, align="C")
    pdf.cell(160, 10, "Dr. G. S. Gill (Founder)", ln=True, align="R")
    
    pdf.set_y(160)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Bharat AI School - Empowering Builders", ln=True, align="C")
    
    # Output to bytes
    return pdf.output(dest='S').encode('latin-1')
