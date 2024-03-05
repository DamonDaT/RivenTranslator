import os

from dotenv import load_dotenv
from flask import Flask, request, send_file, jsonify

from src.translator import PDFTranslator
from src.utils import ArgumentParser, Configurator, root_logger

TEMP_FILE_DIR = "flask_temps/"

app: Flask = Flask(__name__)


def init_app() -> Flask:
    translator = create_translator()

    @app.route('/translation', methods=['POST'])
    def translation():
        try:
            input_file = request.files['input_file']
            source_language = request.form.get('source_language', 'English')
            target_language = request.form.get('target_language', 'Chinese')

            root_logger.info("input_file: %s", input_file)
            root_logger.info("input_file.filename: %s", input_file.filename)

            if input_file and input_file.filename:
                # 创建临时文件
                input_file_path = TEMP_FILE_DIR + input_file.filename
                root_logger.info("input_file_path: %s", input_file_path)

                input_file.save(input_file_path)

                output_file_path = translator.translate_pdf(
                    input_file=input_file_path,
                    source_language=source_language,
                    target_language=target_language)

                # 移除临时文件
                os.remove(input_file_path)

                # 构造完整的文件路径
                output_file_path = os.getcwd() + "/" + output_file_path
                root_logger.info(output_file_path)

                # 返回翻译后的文件
                return send_file(output_file_path, as_attachment=True)
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
            return jsonify(response), 400

    return app


def create_translator() -> PDFTranslator:
    # Arguments
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    configs = Configurator()
    configs.initialize(args)

    return PDFTranslator(configs.model_name)


if __name__ == "__main__":
    # Initialize environment variables from .env file
    load_dotenv(verbose=True)

    app = init_app()
    app.run(host="0.0.0.0", port=5000)
