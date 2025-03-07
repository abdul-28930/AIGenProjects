from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from typing import Dict, List
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            spaceBefore=30
        ))

        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20
        ))

        # Content style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))

    def generate_pdf(
        self, 
        title: str, 
        sections: List[Dict], 
        contents: Dict[str, Dict[str, str]], 
        output_path: str
    ) -> str:
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Build the document
            story = []

            # Add title
            story.append(Paragraph(title, self.styles['CustomTitle']))
            story.append(Spacer(1, 30))

            # Add sections
            for section in sections:
                # Add main heading
                story.append(Paragraph(section['heading'], self.styles['CustomHeading']))
                
                # Add main heading content
                if section['heading'] in contents:
                    story.append(Paragraph(
                        contents[section['heading']]['main'], 
                        self.styles['CustomBody']
                    ))

                # Add subheadings and their content
                for subheading in section['subheadings']:
                    story.append(Paragraph(subheading, self.styles['CustomSubHeading']))
                    if section['heading'] in contents and subheading in contents[section['heading']]:
                        story.append(Paragraph(
                            contents[section['heading']][subheading], 
                            self.styles['CustomBody']
                        ))

            # Build the PDF
            doc.build(story)
            return output_path

        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None 