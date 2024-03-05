# -*- coding: utf-8 -*-
# Author: Riven.FDT
# Description: [translator] Create TranslatorChain based on LLMChain.

from langchain.chains import LLMChain

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain_openai import ChatOpenAI

from src.utils import translator_logger


class TranslatorChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", verbose: bool = True):

        # System
        system_template = (
            """You are a translation expert, proficient in various languages. \n
            Translates {source_language} to {target_language}."""
        )
        system_message_prompt_template = SystemMessagePromptTemplate.from_template(system_template)

        # Human
        human_template = "{text}"
        human_message_prompt_template = HumanMessagePromptTemplate.from_template(human_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt_template, human_message_prompt_template]
        )

        # Model. For stability of translation results, set temperature to 0.
        chat_model = ChatOpenAI(model_name=model_name, temperature=0, verbose=verbose)

        # Chain
        self.chain = LLMChain(llm=chat_model, prompt=chat_prompt_template, verbose=verbose)

    def invoke(self, text: str, source_language: str, target_language: str) -> (str, bool):
        result = ""

        try:
            result = self.chain.invoke({
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
            })
        except Exception as e:
            translator_logger.error('An error occurred during translation: %s', e)
            return result, False

        return result, True
