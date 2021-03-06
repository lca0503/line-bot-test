import json

def get_qa_dict(context_path):
    with open(context_path, 'r', encoding="utf-8") as reader:
        context = json.load(reader)
    QA_dict = {}
    for c in context:
        for token in c['Question_tokens']:
            QA_dict[token] = c['Answers']
    return QA_dict
