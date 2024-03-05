# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [translator] PDF Translator.

from typing import Optional

from src.translator.pdf_parser import PDFParser
from src.translator.translator_chain import TranslatorChain
from src.translator.writer import Writer
from src.utils import translator_logger


class PDFTranslator:
    def __init__(self, model_name: str):
        self.translator_train = TranslatorChain(model_name)
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(
            self,
            input_file: str,
            output_file_format: str = 'MarkDown',
            source_language: str = "English",
            target_language: str = 'Chinese',
            pages_limit: Optional[int] = None
    ) -> str:

        book = self.pdf_parser.parse_pdf(input_file, pages_limit)

        for page_idx, page in enumerate(book.pages):
            for content_idx, content in enumerate(page.contents):
                # Translate content.original
                translation, status = self.translator_train.invoke(content.original, source_language, target_language)
                translator_logger.info("[translation]\n%s", translation)
                # Update the content in self.books.pages directly
                book.pages[page_idx].contents[content_idx].set_translation(translation['text'], status)

        return self.writer.save_translated_book(book, output_file_format)
