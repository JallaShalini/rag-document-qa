from pathlib import Path
from datetime import date

pdf_path = Path('sample_documents/company_report.pdf')
text = '''Company Report

Executive Summary:
Acme Solutions delivered strong performance in Q2 2026 with growth across product and services. Revenue expanded while operational efficiency improved. Strategic priorities include AI roadmap acceleration and expanded enterprise engagement.

Financial Highlights:
- Revenue: $5.2M, up 16% quarter-over-quarter
- Gross margin: 53%
- Net operating profit: $1.1M

Operations:
- Customer onboarding improved through automation and support enhancements.
- The product team launched the AI insights dashboard ahead of schedule.
- Headcount remained stable while productivity rose.

Strategic Priorities:
- Expand enterprise ARR with targeted sales campaigns.
- Optimize support workflows to maintain satisfaction above 92%.
- Accelerate AI-powered summarization features for the next release.

Prepared by: Finance and Strategy Team
Date: ''' + date.today().isoformat() + '\n'''

content_lines = text.split('\n')
text_stream = b''
for idx, line in enumerate(content_lines):
    if idx == 0:
        text_stream += f'BT /F1 18 Tf 50 740 Td ({line}) Tj ET\n'.encode('utf-8')
    else:
        y = 740 - 18 * idx
        if y < 50:
            break
        text_stream += f'BT /F1 12 Tf 50 {y} Td ({line}) Tj ET\n'.encode('utf-8')

contents = b'<< /Length %d >>\nstream\n%s\nendstream' % (len(text_stream), text_stream)
objects = [
    b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n',
    b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n',
    b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n',
    b'4 0 obj\n' + contents + b'\nendobj\n',
    b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n',
]

pdf = b'%PDF-1.4\n'
start_offsets = []
for obj in objects:
    start_offsets.append(len(pdf))
    pdf += obj
xref = b'xref\n0 %d\n0000000000 65535 f \n' % (len(objects) + 1)
for offset in start_offsets:
    xref += b'%010d 00000 n \n' % offset
pdf += xref
pdf += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%EOF\n' % (len(objects) + 1, len(pdf))
pdf_path.write_bytes(pdf)
print(f'Created PDF: {pdf_path} ({pdf_path.stat().st_size} bytes)')
