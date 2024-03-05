# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [translator] PDF Writer.

from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak

from src.books import Book, ContentType
from src.utils import translator_logger


class Writer:
    def __init__(self):
        pass

    def save_translated_book(self, book: Book, output_file_format: str):
        if output_file_format.lower() == "pdf":
            output_file_path = self._save_translated_book_pdf(book)
        elif output_file_format.lower() == "markdown":
            output_file_path = self._save_translated_book_markdown(book)
        else:
            translator_logger.error("Unsupported file format: %s", output_file_format)
            return ""
        return output_file_path

    @staticmethod
    def _save_translated_book_pdf(book: Book):
        output_file_path = book.pdf_file_path.replace('.pdf', f'_translated.pdf')
        translator_logger.info("Start exporting to %s", output_file_path)

        # Register Chinese font
        font_path = "/home/dateng/code/LLM_Projects_ssh/Translator/conf/simsun.ttc"
        pdfmetrics.registerFont(TTFont("SimSun", font_path))

        # Create a new ParagraphStyle with the SimSun font
        simsun_style = ParagraphStyle('SimSun', fontName='SimSun', fontSize=12, leading=14)

        # Create a PDF document
        doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter, encoding="utf-8")
        story = []

        # Iterate over the pages and contents
        for page in book.pages:
            for content in page.contents:
                if content.status:
                    if content.content_type == ContentType.TEXT:
                        # Add translated text to the PDF
                        text = content.translation
                        para = Paragraph(text, simsun_style)
                        story.append(para)

                    elif content.content_type == ContentType.TABLE:
                        # Add table to the PDF
                        tables = content.translation
                        table_style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),
                            ('FONTSIZE', (0, 0), (-1, 0), 14),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ])
                        for table in tables:
                            pdf_table = Table(table)
                            pdf_table.setStyle(table_style)
                            story.append(pdf_table)
            # Add a page break after each page except the last one
            if page != book.pages[-1]:
                story.append(PageBreak())

        # Save the translated book as a new PDF file
        doc.build(story)
        return output_file_path

    @staticmethod
    def _save_translated_book_markdown(book: Book):
        output_file_path = book.pdf_file_path.replace('.pdf', f'_translated.md')
        translator_logger.info("Start exporting to %s", output_file_path)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Iterate over the pages and contents
            for page in book.pages:
                for content in page.contents:
                    if content.status:
                        if content.content_type == ContentType.TEXT:
                            # Add translated text to the Markdown file
                            text = content.translation
                            output_file.write(text + '\n\n')

                        elif content.content_type == ContentType.TABLE:
                            # Add table to the Markdown file
                            tables = content.translation
                            for table in tables:
                                header = '| ' + ' | '.join(str(column) for column in table[0]) + ' |' + '\n'
                                separator = '| ' + ' | '.join(['---'] * len(table[0])) + ' |' + '\n'
                                body = '\n'.join(
                                    ['| ' + ' | '.join(str(cell) for cell in row) + ' |' for row in table[1:]]) + '\n\n'
                                output_file.write(header + separator + body)

                # Add a page break (horizontal rule) after each page except the last one
                if page != book.pages[-1]:
                    output_file.write('---\n\n')

        return output_file_path
