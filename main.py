import re
from pprint import pprint
import csv

if __name__ == '__main__':
    # читаем адресную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    pprint(contacts_list)
    contacts_list_new = []
    contacts_list_new.append(contacts_list[0])
    # Добавил поле "full_name" для удобства поиска совпадений фамилий и имен и для наведения порядка в ФИО
    contacts_list_new[0].append('full_name')
    # Приводим в порядок ФИО.
    for i in range(1, len(contacts_list)):
        contacts_list_new.append(contacts_list[i])
        contacts_list_new[i].append(' '.join(contacts_list[i][:3]))
        contacts_list_new[i][1] = contacts_list_new[i][7].split(' ')[1]
        contacts_list_new[i][2] = contacts_list_new[i][7].split(' ')[2]
        contacts_list_new[i][0] = contacts_list_new[i][7].split(' ')[0]
        # Собираем цифры из поля "Телефон" чтоб получить информацию о наличии дополнительного номера
        r_phone_number = ''.join(re.findall(r'\d+', contacts_list_new[i][5]))
        len_phone_number = len(r_phone_number)
        if len(r_phone_number) == 15:
            pattern = r'^(\+7|7|8)?\s*\(?(\d{3})\)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})[^\d\+]*(\d{4}).*'
            repl = r'+7(\2)\3-\4-\5 доб.\6'
            contacts_list_new[i][5] = re.sub(pattern, repl, contacts_list_new[i][5])
        elif len(r_phone_number) == 11:
            pattern = r'^(\+7|7|8)?\s*\(?(\d{3})\)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2}).*'
            repl = r'+7(\2)\3-\4-\5'
            contacts_list_new[i][5] = re.sub(pattern, repl, contacts_list_new[i][5])
    # Проверка на дубликаты записей
    double_string = True
    while double_string:
        n_of_double_string = {}
        for i, j in enumerate(contacts_list_new):
            for k in range(1, len(contacts_list_new)):
                if j[0] in contacts_list_new[k][7] and j[1] in contacts_list_new[k][7] and i != k:
                    if i not in n_of_double_string and k not in n_of_double_string:
                        n_of_double_string[i] = k
                        break
        # Если есть дубли записей, то переносим недостающую информацию
        if len(n_of_double_string) != 0:
            for i in n_of_double_string:
                for j in range(len(contacts_list_new[i])):
                    if contacts_list_new[i][j] == '' and contacts_list_new[n_of_double_string[i]][j] != '':
                        contacts_list_new[i][j] = contacts_list_new[n_of_double_string[i]][j]
            # Удаляем дубликаты
            for i in sorted(list(n_of_double_string), reverse=True):
                del contacts_list_new[n_of_double_string[i]]
            n_of_double_string = {}
        else:
            double_string = False
    # Удаляем колонку "full_name"
    for i in contacts_list_new:
        del i[7]
    pprint(contacts_list_new)
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list_new)
