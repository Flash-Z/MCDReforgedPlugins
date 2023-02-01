import os
from mcdreforged.api.rtext import *
from todolist.operate_list import operate_list

from todolist.functions import functions as fun
from todolist.UI import prefix

def on_load(server,old):
    server.register_help_message(f'{prefix}', RText('ToDoList').h('点击查看帮助'))
    if not os.path.isfile(fun.todolist_path):
        fun.save()
    else:
        try:
            fun.read()
        except Exception as e:
            server.say('§b[ToDoList]§4配置加载失败，请确认配置路径是否正确：{}'.format(e))
            
def on_info(server, info):
    if info.is_user:
        if info.content.startswith(prefix):
            info.cancel_send_to_server()
            args = info.content.split(' ')
            operate_list(server, info, args)
            
def on_server_stop(server, return_code):
    pass