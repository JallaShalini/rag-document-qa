from pathlib import Path


PROMPT_TEMPLATE_PATH = Path(__file__).resolve().parent.parent / 'prompts' / 'rag_prompt.txt'


def build_prompt(context_chunks: list[str], question: str) -> str:
    context = '\n\n'.join(context_chunks)
    template = PROMPT_TEMPLATE_PATH.read_text(encoding='utf-8')
    return template.format(context=context, question=question)
