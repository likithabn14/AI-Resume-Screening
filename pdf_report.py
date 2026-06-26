from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

styles = getSampleStyleSheet()


def generate_pdf(
    filename,
    match_percentage,
    ats_score,
    recommendation,
    matched_skills,
    missing_skills,
    suggestions
):

    doc = SimpleDocTemplate(filename)

    elements = []

    elements.append(
        Paragraph("<b><font size=20>AI Resume Screening Report</font></b>", styles["Title"])
    )

    elements.append(
        Paragraph(f"<b>Resume Match:</b> {match_percentage}%", styles["Normal"])
    )

    elements.append(
        Paragraph(f"<b>ATS Score:</b> {ats_score}/100", styles["Normal"])
    )

    elements.append(
        Paragraph(f"<b>Recommendation:</b> {recommendation}", styles["Normal"])
    )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    # -----------------------------
    # Matching Skills
    # -----------------------------

    elements.append(
        Paragraph("<b>Matching Skills</b>", styles["Heading2"])
    )

    if matched_skills:

        for skill in matched_skills:

            elements.append(
                Paragraph(f"• {skill}", styles["Normal"])
            )

    else:

        elements.append(
            Paragraph("No matching skills found.", styles["Normal"])
        )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    # -----------------------------
    # Missing Skills
    # -----------------------------

    elements.append(
        Paragraph("<b>Missing Skills</b>", styles["Heading2"])
    )

    if missing_skills:

        for skill in missing_skills:

            elements.append(
                Paragraph(f"• {skill}", styles["Normal"])
            )

    else:

        elements.append(
            Paragraph("No missing skills.", styles["Normal"])
        )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    # -----------------------------
    # Suggestions
    # -----------------------------

    elements.append(
        Paragraph("<b>Suggestions</b>", styles["Heading2"])
    )

    if missing_skills:

        for skill in missing_skills:

            elements.append(
                Paragraph(
                    f"• Learn or add <b>{skill}</b> to improve your resume.",
                    styles["Normal"]
                )
            )

    if suggestions:

        for suggestion in suggestions:

            elements.append(
                Paragraph(
                    f"• {suggestion}",
                    styles["Normal"]
                )
            )

    if not missing_skills and not suggestions:

        elements.append(
            Paragraph(
                "🎉 Excellent Resume! No major improvements needed.",
                styles["Normal"]
            )
        )

    doc.build(elements)