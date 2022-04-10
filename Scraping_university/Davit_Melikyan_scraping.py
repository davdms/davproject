import json

import requests
from bs4 import BeautifulSoup


def get_html():
    response = requests.get('https://cwur.org/2021-22.php', headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'})

    if response.status_code == 200:
        response_html = response.text
        with open('universities.html', 'w', encoding='UTF8') as f:
            f.write(response_html)
    else:
        raise Exception('Exception error')


def get_universities_list():
    response = requests.get('https://cwur.org/2021-22.php', headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'})

    response_html = response.text
    soup = BeautifulSoup(response_html, 'html.parser')
    university_list = soup.find('div', {'class': 'table-responsive'}).find('tbody').select('tr')
    un_list = []
    for un in university_list:
        university_num = un.find('td').text
        university_name = un.find('a').text
        university_country = un.find_all('a')[1].text
        university_score = un.find_all('td')[8].text
        un_list.append({
            'id': university_num,
            'Name': university_name,
            'Country': university_country,
            'Score': university_score
        })
    return un_list


def write_in_csv(unlist):
    with open('universities.csv', 'w', encoding='UTF8') as f:
        f.write('id,Name,Country,Score\n')
        for un in unlist:
            f.write(f'{un["id"]},{un["Name"]},{un["Country"]},{un["Score"]}\n')


def write_in_json(unlist):
    with open('universities.json', 'w', encoding='UTF8') as f:
        f.write(json.dumps(unlist, ensure_ascii=False))

universities_list = get_universities_list()
# write_in_csv(universities_list)
write_in_json(universities_list)
