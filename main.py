import re
from pprint import pprint
import csv


if __name__ == '__main__':
    # читаем адресную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # rewriting phone numbers
    phone_num = r'(\+7|8)\s?\(?(\w{3})\)?\s?-?(\w{3})-?(\w{2})-?(\w{2})(\s?)(\(?((доб\.)\s(\w{4}))\)?)?'
    num_format = r'+7(\2)\3-\4-\5\6\9\10'

    i = 1
    form_list = contacts_list
    while i < len(contacts_list):
        form_list[i][5] = re.sub(phone_num, num_format, contacts_list[i][5])
        i += 1


    # pprint(form_list)


    # put names, surnames... as different elements
    def arrange_names(some_list):
        new_list = some_list

        for n in range(0, 2):
            for i in range(1, 9):
                if re.search(r'\s', some_list[i][n]):
                    name = some_list[i][n].split(' ')
                    if n == 0:
                        if some_list[i][1] != '':
                            name.extend(some_list[i][3:])
                            new_list[i] = name
                        else:
                            name.extend(some_list[i][2:])
                            new_list[i] = name
                    else:
                        new_list[i][n] = name[0]
                        new_list[i][n + 1] = name[1]
                else:
                    pass

        return new_list


    phone_list = arrange_names(form_list)

    # notice that organization is in the wrong place in most cases
    for i in range(len(phone_list)):
        if phone_list[i][3] == '' and phone_list[i][4] != '':
            phone_list[i][3] = phone_list[i][4]
            phone_list[i][4] = ''
        else:
            pass

    # notice that position is also in wrong place for some
    for i in range(len(phone_list)):
        if phone_list[i][4] == '' and phone_list[i][5] != '':
            phone_list[i][4] = phone_list[i][5]
            phone_list[i][5] = ''
        else:
            pass

    # notice that due to the names' rearrangement all items except [3] have an additional inner item ([i][5])
    phone_list[3][5] = phone_list[3][4]
    phone_list[3][4] = ''

    for i in range(1, 8):
        if phone_list[i][5] == '':
            phone_list[i].pop(5)

    # search for same name (in our case the similarity between last names is enough)
    # add new info from the second person to the first one with the same name where first has empty spaces
    for i in range(1, 9):
        for n in range(1, (len(phone_list) - i)):
            if phone_list[i][0] == phone_list[i + n][0]:
                for m in range(3, 7):
                    if phone_list[i][m] == '':
                        phone_list[i][m] = phone_list[i + n][m]
                    else:
                        pass
            else:
                pass

    # now second copies of people don't have any valuable/new info, we can delete them
    # make list of people to delete
    ind_del = []
    for i in range(1, 9):
        for n in range(1, (len(phone_list) - i)):
            if phone_list[i][0] == phone_list[i + n][0]:
                ind_del.append(i + n)
            else:
                pass

    # delete copies with an understanding that each successful deletion will shorten the index range in our final list
    for i in ind_del:
        if len(phone_list) == 9:
            phone_list.pop(i)
        else:
            phone_list.pop(i - (9 - len(phone_list)))

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(phone_list)
