import os
import json
import requests
import pandas as pd
from fake_useragent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}

ua = UserAgent()
FAKE_HEADERS = {
    'User-Agent': ua.chrome
}

def crawl_text_and_images(url, headers= HEADERS, is_save=False):
    response = requests.get(url, headers= headers)
    print("RESPONSE: ", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    def crawl_text():
        nonlocal soup, url
        title = soup.find("div", {"class": "ArticleView-title"})

        summary = soup.find("div", {"class": "ArticleView-summary"})

        content = soup.find("div", {"class": "ArticleView-text"})
        content_p_tag = content.find_all("p", recursive=False)
        all_text = ""
        for p_tag in content_p_tag:
            if p_tag.text.strip() != '':
                all_text += f'{p_tag.text}\n'

        return {
            "title": title.text.strip(),
            "summary": summary.text.strip(),
            "content": all_text.strip()
        }
    
    def crawl_image(is_save=False):
        nonlocal soup, url
        wrap_images =  soup.find_all("picture")
        # print(wrap_image[1]) 
        img_list = []  
        
        for index, image in enumerate(wrap_images):
            if 'Card-picture' in image.find_parent()['class']:
                continue
            img_url = image.find('img')['data-src']
            if is_save:
                if not os.path.exists('save_image'):
                    os.makedirs('save_image')
                img_list.append(img_url.split('/')[-1])
                urlretrieve(img_url, 'save_image/' + img_url.split('/')[-1]) 
    # crawl_text()
        return {
            "image_list": img_list
        }
    information = crawl_text()
    img_infor = crawl_image(is_save)
    information.update(img_infor)
    return information


if __name__ == "__main__":
    df = pd.read_csv('data/RT_train.csv')
    url_list = list(df.iloc[:, 1])
    # print(list(df.iloc[:5, 1]))
    output_list = []
    for index, url in tqdm(enumerate(url_list)):
        print(index, url)
        output_dict = crawl_text_and_images(url, is_save=True)
        output_list.append(output_dict)

        if index == 3: break
    with open('output_dict.json', 'w+', encoding='utf-8') as f:
        json.dump(output_list, f, ensure_ascii=False)
    

