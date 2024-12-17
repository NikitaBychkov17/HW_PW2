import csv
import re
from pprint import pprint

# Чтение адресной книги из CSV файла
with open("Проф_работа\Да\phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Приведение ФИО к единому формату
def normalize_names(contacts):
    for contact in contacts:
        full_name = " ".join(contact[:3]).split()
        if len(full_name) == 3:
            contact[0], contact[1], contact[2] = full_name
        elif len(full_name) == 2:
            contact[0], contact[1], contact[2] = full_name[0], full_name[1], ''
    return contacts

# Приведение телефонов к единому формату
def normalize_phones(contacts):
    phone_pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*доб\.\s*(\d+))?")
    formatted_phone = r"+7(\2)\3-\4-\5 доб.\7"
    for contact in contacts:
        contact[5] = phone_pattern.sub(formatted_phone, contact[5]).replace(' доб. ', '') if 'доб.' not in contact[5] else phone_pattern.sub(formatted_phone, contact[5])
    return contacts

# Удаление дублей
def remove_duplicates(contacts):
    contacts_dict = {}
    for contact in contacts:
        name_key = (contact[0], contact[1])
        if name_key not in contacts_dict:
            contacts_dict[name_key] = contact
        else:
            for i in range(2, 7):
                if not contacts_dict[name_key][i] and contact[i]:
                    contacts_dict[name_key][i] = contact[i]
    return list(contacts_dict.values())

# Вызов функций для выполнения задания
contacts_list = normalize_names(contacts_list)
contacts_list = normalize_phones(contacts_list)
contacts_list = remove_duplicates(contacts_list)

# Печать итогового списка для проверки
pprint(contacts_list)

# Запись результата в новый CSV файл
with open("Проф_работа\Да\phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
