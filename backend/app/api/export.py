from __future__ import annotations

import io
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.schemas import ExportReportRequest

router = APIRouter()


def _wrap_text(text: str, max_chars: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current: List[str] = []
    current_len = 0
    for w in words:
        next_len = (current_len + len(w) + (1 if current else 0))
        if next_len > max_chars and current:
            lines.append(" ".join(current))
            current = [w]
            current_len = len(w)
        else:
            current.append(w)
            current_len = next_len
    if current:
        lines.append(" ".join(current))
    return lines


@router.post("/export")
async def export_pdf(payload: ExportReportRequest) -> Response:
    try:
        rec = payload.recommendation

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        y = height - 56
        x = 52
        c.setFont("Helvetica-Bold", 16)
        c.drawString(x, y, "AlgoVista AI – Algorithm Recommendation Report")

        y -= 28
        c.setFont("Helvetica", 11)
        c.drawString(x, y, f"Recommended Algorithm: {rec.recommended_algorithm}")
        y -= 18
        c.drawString(x, y, f"Time Complexity: {rec.time_complexity}")
        y -= 18
        c.drawString(x, y, f"Space Complexity: {rec.space_complexity}")

        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, "Why this algorithm?")
        y -= 16
        c.setFont("Helvetica", 10)
        for line in _wrap_text(rec.reason, max_chars=104):
            c.drawString(x, y, line)
            y -= 14
            if y < 70:
                c.showPage()
                y = height - 56
                c.setFont("Helvetica", 10)

        y -= 6
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, "Alternative Algorithms")
        y -= 16

        c.setFont("Helvetica", 10)
        for alt in rec.alternatives[:10]:
            c.drawString(x, y, f"- {alt.algorithm} | {alt.time_complexity} | {alt.space_complexity}")
            y -= 14
            for line in _wrap_text(alt.short_reason, max_chars=104):
                c.drawString(x + 14, y, line)
                y -= 12
                if y < 70:
                    c.showPage()
                    y = height - 56
                    c.setFont("Helvetica", 10)

        c.showPage()
        c.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=AlgoVistaAI_Report.pdf"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

