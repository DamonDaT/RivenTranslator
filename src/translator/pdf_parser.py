# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [translator] Parse pdf files based on pdfplumber.

import pdfplumber
from typing import Optional

from src.books import Book, Page, Content, ContentType, TableContent
from src.translator.exceptions import PageOutOfRangeException
from src.utils import translator_logger


class PDFParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_pdf(pdf_file_path: str, pages_limit: Optional[int] = None) -> Book:
        translator_logger.info("Start parsing file: %s", pdf_file_path)

        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages_limit is not None and pages_limit > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages_limit)

            if pages_limit is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages_limit]

            for pdf_page in pages_to_parse:
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text()
                tables = pdf_page.extract_tables()

                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    translator_logger.info("[raw_text]\n%s", cleaned_raw_text)

                # Handling tables
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    translator_logger.info("[table]\n%s", table)

                book.add_page(page)

        return book
