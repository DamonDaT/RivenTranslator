import gradio

from dotenv import load_dotenv

from src.translator import PDFTranslator
from src.utils import ArgumentParser, Configurator, root_logger

Translator: PDFTranslator


def translation(input_file, source_language, target_language):
    root_logger.info("[Gradio Server] 开始翻译任务\n源文件: %s\n源语言: %s\n目标语言: %s",
                     (input_file.name, source_language, target_language))

    output_file_path = Translator.translate_pdf(
        input_file.name,
        source_language=source_language,
        target_language=target_language
    )

    root_logger.info("[Gradio Server] 翻译任务结束")

    return output_file_path


def launch_gradio():
    iface = gradio.Interface(
        fn=translation,
        title="Riven-Translator(PDF 电子书翻译工具)",
        inputs=[
            gradio.File(label="上传PDF文件"),
            gradio.Textbox(label="源语言（默认：英文）", placeholder="English", value="English"),
            gradio.Textbox(label="目标语言（默认：中文）", placeholder="Chinese", value="Chinese")
        ],
        outputs=[
            gradio.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")


def initialize_translator() -> None:
    # Arguments
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    configs = Configurator()
    configs.initialize(args)

    global Translator
    Translator = PDFTranslator(configs.model_name)


if __name__ == "__main__":
    # Initialize environment variables from .env file
    load_dotenv(verbose=True)
    # Initialize translator
    initialize_translator()
    # Launch Gradio Server
    launch_gradio()
