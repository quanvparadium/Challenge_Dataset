from googletrans import Translator
import json
from tqdm import tqdm

def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def process_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def test():
    original_text = "Chào bạn, đây là một ví dụ về việc dịch với Google Translate."
    translated_text = translate_text(original_text, target_language='en')

    print(f'Original text: {original_text}')
    print(f'Translated text: {translated_text}')

if __name__ == "__main__":
    translator = Translator()
    data = process_file("output_dict.json")
    original_text = data[0]['title']
    new_data = []
    for paper in tqdm(data):
        new_data.append({
            'title': translator.translate(paper['title'], dest='en').text,
            'summary': translator.translate(paper['summary'], dest='en').text,
            'content': translator.translate(paper['content'], dest='en').text,
            "image_list": paper['image_list']
        })
    with open('output_dict_new.json', 'w+', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False)
    # test()
