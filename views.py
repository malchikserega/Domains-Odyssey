from app import app
from flask import render_template, request, Response
import db_functions
from scripts.scrap import screen


@app.route('/', methods=["GET", "POST"])
def some():
    """
    Функция возвращает главную страницу
    :rtype: Response
    :return: Главная страница
    """
    return render_template('base.html',
                           title='Main')


@app.route('/domains', methods=['GET', 'POST'])
def domains():
    """
    Если метод GET:
        Функция возвращает страницу доменов
    Если метод POST:
        Функция обновляет таблицу доменов и
         возвращает страницу доменов
    :rtype: Response
    :return: Страница доменов
    """
    if request.method == 'POST':
        db_functions.update_domains()
    return render_template('domains.html',
                           title='Domains',
                           lines=db_functions.show_all_domains()
                           )


@app.route('/whitelist', methods=['GET', 'POST'])
def whitelist():
    """
    Если метод GET:
        Функция возвращает страницу белых доменов
    Если метод POST:
        Принимает файл

        Функция обновляет таблицу белых доменов и
         возвращает страницу белых доменов
    :rtype: Response
    :return: Страница белых доменов
    """
    if request.method == 'POST':
        file = request.files['file']
        lines = (line.decode('UTF-8').rstrip('\n').rstrip('\r').rstrip(',') for line in file.readlines())
        db_functions.update_whitelist(lines)
    return render_template('whitelist.html',
                           title='Whitelist',
                           lines=db_functions.show_all_whitelist()
                           )


@app.route('/filtered', methods=['GET', 'POST'])
def filtered():
    """
    Если метод GET:
        Функция возвращает страницу с отфильтрованными доменами
    Если метод POST:
        Два поля: Содержимое поля поиска и чекбокс

        Функция обновляет таблицу отфильтрованных доменов и
        возвращает страницу с доменами соответствующими поиску и
        отфильтрованными(которых нет в белом списке доменов) доменами
    :rtype: Response
    :return: Страницы
    """
    lines = []
    if request.method == 'POST':
        text = request.form['text']
        regexp = 'regexp' in request.form and request.form['regexp'] == 'on'

        # lines - 1 таблица
        lines = db_functions.search_domains(text=text, regexp=regexp)
        # updated - 2 таблица либо false
        updated = db_functions.update_filtered(lines)
    else:
        updated = db_functions.get_filtered()
    return render_template('filtered.html',
                           title='Filtered',
                           table1=lines,
                           table2=updated)


@app.route('/results', methods=["GET", "POST"])
def results():
    """
    Если метод GET:
        Функция возвращает страницу результатов
    Если метод POST:
        Функция обновляет таблицу результатов и
        возвращает страницу результатов
    :rtype: Response
    :return: Страница результатов
    """
    if request.method == 'POST':
        lines = db_functions.get_filtered()
        table = screen(lines)
        db_functions.update_results(table)
    lines = db_functions.get_results()
    return render_template('result.html',
                           title='Results',
                           lines=lines)


@app.route('/img/<name>')
def show_img(name):
    """
    Функция возврращает картинку по имени домена из таблицы результатов
    :param name: Имя домена
    :rtype: Response
    :return: Ответ с картинкой (массив байтов)
    """
    photo = db_functions.get_photo(name)
    return Response(photo, 200, {'Content-Type': 'image/png'})


app.run('0.0.0.0', 5000, True)
