from app import db
import models
from scripts import scrap


def delete_table(table_name):
    """
    Функция удаляет таблицу по имени
    :param table_name: Имя таблицы
    :rtype: int
    :return: Количество удаленых строк
    """
    assert table_name in ['domains', 'Domains', 'whitelist', 'Whitelist', 'filtered', 'Filtered', 'results', 'Results']
    try:
        if table_name in ['domains', 'Domains']:
            models.Domains.query.delete()
        elif table_name in ['whitelist', 'Whitelist']:
            models.Whitelist.query.delete()
        elif table_name in ['filtered', 'Filtered']:
            models.Filtered.query.delete()
        elif table_name in ['results', 'Results']:
            models.Results.query.delete()
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def show_all_domains():
    """
    Функция возвращает все домены из таблицы доменов
    :rtype: list
    :return: список доменов
    """
    query_result = models.Domains.query.all()
    return [ent.name for ent in query_result]


def add_list_domains(names):
    """
    Добавляет в таблицу список доменов
    :param names: Список доменов
    :rtype: bool
    :return: В случае успешного выполнения - True
    В случае неуспешного выполнения - False
    """
    try:
        for name in names:
            new_one = models.Domains(name)
            db.session.add(new_one)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def update_domains():
    """
    Обновляет таблицу доменов
    :rtype: bool
    :return: В случае успешного выполнения - True
    В случае неуспешного выполнения - False
    """
    rows = scrap.get_all_domains()
    if rows and delete_table('Domains') and add_list_domains(rows):
        return True
    return False


def update_whitelist(names):
    """
    Обновляет таблицу белых доменов
    :rtype: bool
    :return: В случае успешного выполнения - True
    В случае неуспешного выполнения - False
    """
    try:
        if not delete_table('Whitelist'):
            return False
        for name in names:
            new_one = models.Whitelist(name)
            db.session.add(new_one)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def show_all_whitelist():
    """
    Функция возвращает все белые домены из таблицы белых доменов
    :rtype: list
    :return: список доменов
    """
    query_result = models.Whitelist.query.all()
    return [ent.name for ent in query_result]


def search_domains(text, regexp):
    """
    Функция возвращает совпадения доменов из таблицы доменов с заданым пользователем
    регулярным выражением или словом
    :param text: Слово
    :param regexp: Регулярное выражение
    :rtype: list
    :return: Список совпадений
    """
    domains = db.session.query(models.Domains).all()
    if not regexp:
        domains = [domain for domain in domains if text in domain.name]
    else:
        domains = [domain for domain in domains if scrap.check_reg(domain.name, text, True)]
        # query = query.filter(models.Domains.name.op('regexp')(text))
    lines = [line.name for line in domains]
    return lines


def add_list_filtered(names):
    """
    Добавляет домены в таблицу отфильтрованных доменов
    :param names: Список доменов
    :rtype: bool
    :return: В случае успешного выполнения - True
    В случае неуспешного выполнения - False
    """
    try:
        for name in names:
            new_one = models.Filtered(name)
            db.session.add(new_one)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def update_filtered(lines):
    """
    Очистка базы отфильтрованных ранее доменов
    Добавляет в базу отфильтрованных доменов которых в таблице белых доменов
    :param lines: Список доменов
    :rtype: list or bool
    :return: Список доменов или False - в результате ошибки доавления в таблицу
    """
    if not delete_table('Filtered'):
        return False
    base_query = models.Whitelist.query
    filtered = []
    for line in lines:
        # TODO exist better
        count = base_query.filter(models.Whitelist.name == line).count()
        if not count:
            filtered += [line]
    if add_list_filtered(filtered):
        return filtered
    return False


def get_filtered():
    """
    Функция возвращает список отфильтрованных доменов
    :rtype: list
    :return: список доменов
    """
    values = models.Filtered.query.all()
    lines = [val.name for val in values]
    return lines


def add_list_results(lines):
    """
    Добавляет домены в таблицу результатов
    :param lines: Список доменов в формате [[имя домена, описание, скриншот главной страницы]]
    :rtype: bool
    :return: В случае успешного выполнения - True
    В случае неуспешного выполнения - False
    """
    try:
        for line in lines:
            new_one = models.Results(line)
            db.session.add(new_one)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def update_results(lines):
    """
    Очистка базы результатов
    Добавляет в базу результатов домены которых в таблице белых доменов
    :param lines: Список доменов в формате [[имя домена, описание, скриншот главной страницы]]
    :rtype: bool
    :return: В случае успешного выполнения - True
    В случае неуспешного выполнения - False
    """
    if not delete_table('Results'):
        return False
    if add_list_results(lines):
        return True
    return False


def get_results():
    """
    Функция возвращает имя и описание домена
    :rtype: list of list
    :return: список доменов в формате [[имя домена, описание]]
    """
    values = models.Results.query.all()
    lines = [[val.name, val.description] for val in values]
    return lines


def get_photo(name):
    """
    Функция возвращает фотографию домена по его имени
    :param name: Имя домена
    :rtype: bytearray
    :return: Фото
    """
    ph = models.Results.query.filter(models.Results.name == name).first()
    return ph.img
