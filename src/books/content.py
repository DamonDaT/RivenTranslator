# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [books] Content class.

from enum import Enum, auto
from PIL import Image as PILImage

from src.utils import translator_logger


class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()


class Content:
    def __init__(self, content_type, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, list):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False


class TableContent(Content):
    def __init__(self, data):
        super().__init__(ContentType.TABLE, str(data))

    def set_translation(self, translation, status):
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            # Convert the string to a list of lists
            tables_data = eval(translation.strip())
            self.translation = tables_data
            self.status = status
        except Exception as e:
            translator_logger.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def iter_items(self, translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        return self.original.to_string(header=False, index=False)
