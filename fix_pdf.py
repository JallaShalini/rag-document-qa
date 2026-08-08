import os
from reportlab.pdfgen import canvas

pdf_path = os.path.join("sample_documents", "company_report.pdf")
c = canvas.Canvas(pdf_path)

c.setFont("Helvetica-Bold", 16)
c.drawString(50, 800, "Company Report")

c.setFont("Helvetica", 12)
text = [
    "Executive Summary:",
    "Acme Solutions delivered strong performance in Q2 2026 with growth across product",
    "and services. Revenue expanded while operational efficiency improved.",
    "",
    "Financial Highlights:",
    "- Revenue: $5.2M, up 16% quarter-over-quarter",
    "- Gross margin: 53%",
    "- Net operating profit: $1.1M",
    "",
    "Operations:",
    "Customer onboarding improved through automation and support enhancements.",
    "The product team launched the AI insights dashboard ahead of schedule.",
    "",
    "Strategic Priorities:",
    "Expand enterprise ARR with targeted sales campaigns and accelerate AI-powered features."
]

y_position = 770
for line in text:
    c.drawString(50, y_position, line)
    y_position -= 20

c.save()
print("Fixed PDF successfully!")
