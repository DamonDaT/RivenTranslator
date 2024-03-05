# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [books] Page class.

from .content import Content


class Page:
    def __init__(self):
        self.contents = []

    def add_content(self, content: Content):
        self.contents.append(content)
