import json
import os

class functions:
    list_dic = {}
    file_path = './config/ToDoList/'
    todolist_path = file_path + 'ToDoList.json'

    def read():
        if(not os.path.exists(functions.file_path)):
            os.mkdir(functions.file_path)
        with open(functions.todolist_path, encoding='utf-8') as f:
            functions.list_dic = json.load(f)

    def save():
        with open(functions.todolist_path, 'w', encoding='utf-8') as f:
            json.dump(functions.list_dic, f, indent=4, ensure_ascii=False)

    def search(name):
        for k, v in functions.list_dic.items():
            if name == k:
                return k