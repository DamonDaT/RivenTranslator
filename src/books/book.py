# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [books] Book class.

from .page import Page


class Book:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.pages = []

    def add_page(self, page: Page):
        self.pages.append(page)
