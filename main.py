# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [Translator] Main file.

from dotenv import load_dotenv

from src.utils import ArgumentParser, Configurator
from src.translator import PDFTranslator

if __name__ == "__main__":
    # Initialize environment variables from .env file
    load_dotenv(verbose=True)

    # Arguments
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    configs = Configurator()
    configs.initialize(args)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(configs.model_name)
    translator.translate_pdf(configs.input_file, configs.output_file_format, pages_limit=None)
