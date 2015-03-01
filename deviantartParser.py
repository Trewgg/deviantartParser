# www.deviantart.com парсер картинок
import os
import urllib.request
from urllib.request import urlretrieve
from bs4 import BeautifulSoup  #установка C:\Python34\Scripts\pip.exe install beautifulsoup4

BASE_URL = 'http://www.deviantart.com/browse/all/contests/2014/diabloiii/?offset=0'  #+24
PATH_CSV = 'links_list.csv'
PATH = 'download'
code_img = ''
num_page = 30
links_img_list = []
links_thumb_list = []

#получаем html-код страницы
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


#парсим внутреннюю страницу
def parse2(html, rid):
    soup = BeautifulSoup(html)
    #ID нужной картинки (img collect_rid="1:434325194")
    collect_rid = '1:' + rid
    #ищем img collect_rid="1:434325194"
    img = soup.find_all('img', collect_rid=collect_rid)
    link2 = ''
    #в этом блоке ищем ссылку src
    for j in img:
        #возвращаем последеюю ссылку в блоке (увеличенную картинку)
        link2 = j['src']
    return link2


#парсим основную страницу
def parse(html):
    soup = BeautifulSoup(html)
    #ищем блок <a class="thumb"
    thumb = soup.find_all('a', class_='thumb')

    num = 1

    #в этом блоке ищем ссылку href
    for i in thumb:
        link_thumb = i['href']
        link_img = ''
        #вырезаем последнии цифры ссылки для collect_rid
        code_img = link_thumb[-9:]

        try:
            #переходим на вторую страницу и парсим ее (ищем ссылку 2)
            link_img = parse2(get_html(link_thumb), code_img)
        except:
            print('Ошибка парсинга второй страницы!')

        print(num, link_thumb, link_img)

        try:
            #сохраняем ссылки в список
            links_img_list.append({link_img})       #вторая ссылка
            links_thumb_list.append({link_thumb})   #первая ссылка
        except:
            print('Ошибка сохранения списка!')

        num += 1

    print('Парсинг закончен!')
    return links_img_list, links_thumb_list


#сохраняем список в файл csv
def save(links_list, path):
    f = open(path, 'w')		#'a'
    for item in links_list:
        #чтобы убрать {, ,} в ссылке
        f.write(''.join(item))
        f.write('\n')
    f.close()
    print('Файл сохранен!')


#скачиваем файл по ссылке из списка
def download(links_list):
    num = 1
    for item in links_list:
        link_tmp = ''.join(item)
        #формирование названия файла
        file_name = PATH + "/" + link_tmp.rsplit('/', 1)[1]

        #проверка на существование файла в папке
        if not os.path.isdir(PATH):
            try:
                #создаем каталог, если его нет
                os.makedirs(PATH)
            except:
                print('Ошибка создания каталога!')
        elif os.path.exists(file_name):
            print("Этот файл уже загружен")
        else:
            try:
                #скачивает файл по ссылке
                urlretrieve(link_tmp, file_name)
            except:
                print('Ошибка скачивания файла!')
        print(num)
        num += 1
    print('Загрузка выполненна!')


def main():
    # i = 0
    # while i <= num_page:
    #     new_url = BASE_URL[:-1] + '%d' % i
    #     parse(get_html(new_url))
	#	  save(links_thumb_list, PATH_CSV)
	#	  download(links_img_list)
    #     i += 24
	#	  print('Страница: ', i)

    parse(get_html(BASE_URL))
    save(links_thumb_list, PATH_CSV)
    download(links_img_list)
    print('Конец!')


if __name__ == '__main__':
    main()