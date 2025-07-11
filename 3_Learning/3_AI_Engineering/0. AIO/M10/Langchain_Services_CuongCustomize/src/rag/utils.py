import re

def extract_answer(text_response: str,
                   pattern: str = r"Answer:\s*(.*)"
                   ) -> str:
    
    match = re.search(pattern, text_response)
    if match:
        answer_text = match.group(1).strip()
        return answer_text
    else:
        return "Answer not found."


