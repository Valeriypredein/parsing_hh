import requests
import json
from fake_headers import Headers
from pprint import pprint
from tqdm import tqdm
from bs4 import BeautifulSoup
import lxml
import bs4

def get_fake_headers():
    return Headers(browser="chrome", os="win").generate()


url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

response = requests.get(url, headers=get_fake_headers())

soup = bs4.BeautifulSoup(response.text, features="lxml")

data = soup.find("main", class_="vacancy-serp-content")

div_tags = data.findAll("div", class_="vacancy-card--H8LvOiOGPll0jZvYpxIF font-inter")


def find_job(tag):
    final_list = []

    for div_tag in tqdm(tag):
        link = div_tag.find("a", class_="bloko-link")["href"]

        if link:
            response = requests.get(link, headers=get_fake_headers())
            vacancy = bs4.BeautifulSoup(response.text, features="lxml")
            vacancy_desc = vacancy.find("div", class_="vacancy-description")
            vacancy_desc_text = " ".join(vacancy_desc.text.split()).lower()

            if ("django" or "flask") in vacancy_desc_text:
                name_vac = div_tag.find("span", class_="serp-item__title-link-wrapper").text
                salary = div_tag.find("span", class_="compensation-text--cCPBXayRjn5GuLFWhGTJ fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj separate-line-on-xs--pwAEUI79GJbGDu97czVC")
                if salary == None:
                    salary = "зарплата не указана"
                else:
                    salary = salary.text
                name_company = div_tag.find("span", class_="company-info-text--O32pGCRW0YDmp3BHuNOP").text
                city = div_tag.find("span", class_="fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj").text

                vacancy_data = {
                    "вакансия": name_vac,
                    "ссылка": link,
                    "зп": salary,
                    "название компании": name_company,
                    "город": city
                }
                final_list.append(vacancy_data)
    return final_list


def record_json(some_list):
    with open("job.json", "w", encoding="utf-8") as f:
        json.dump(some_list, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    final_list = find_job(div_tags)
    record_json(final_list)