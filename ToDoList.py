PLUGIN_METADATA = {
    'id': 'ToDoList',
    'version': '0.1',
    'name': 'ToDoList',  # RText component is allowed
    'description': 'ToDoList',  # RText component is allowed
    'author': 'FangGiGi',
    'link': 'https://github.com/Flash-Z/MCDR-ToDoList',
}

import os
import json
import time
from mcdreforged.api.rtext import *
from mcdreforged.api.decorator import new_thread

prefix = '!!td'
config_path = './config/ToDoList.json'

help_head = """
================== §bToDoList §r==================
以下命令前缀也可只打出首字母，例如(list->l)
""".format(prefix=prefix)
help_body = {
    f"§b{prefix}": "§r显示本帮助信息",
    f"§b{prefix} list": "§r显示ToDoList",
    f"§b{prefix} del <name>": "§r删除<name>",
    f"§b{prefix} reload": "§r重载插件配置",
    f"§b{prefix} add <name> <detail> <progress>": "§r添加/修改名为<name>的项目，参数为描述与进度",
}

list_dic = {}

def read():
    global list_dic
    with open(config_path, encoding='utf-8') as f:
        list_dic = json.load(f)


def save():
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(list_dic, f, indent=4, ensure_ascii=False)

def search(name):
    for k, v in list_dic.items():
        if name == k:
            return k

@new_thread(PLUGIN_METADATA["name"])
def operate_list(server, info, args):
    global list_dic
    
    if len(args) == 1:
        head = [help_head]
        body = [RText(f'{k} {v}\n').c(
            RAction.suggest_command, k.replace('§b', '')).h(v)
                for k, v in help_body.items()]
        server.reply(info, RTextList(*(head + body)))
    
    elif len(args) == 2:
        if args[1] == "list" or args[1] == "l":
            c = ['']

            list_head = RText(f'================== §bToDoList §r==================\n').c(
                RAction.suggest_command, f'!!td list').h(f'§b!!td list\n')
            c.append(list_head)

            for name, list_info in list_dic.items():
                list_msg = RTextList(
                    f'- ',
                    RText(f'[×] ', color = RColor.red).c(RAction.suggest_command, f'!!td del {name}')
                        .h(RText(f'Delete', color = RColor.red)),
                    RText(f'§b{name}').c(RAction.suggest_command, 
                                         f'!!td add {name} {list_dic.get(name)["detail"]} {list_dic.get(name)["progress"]}')
                    .h(
                        f'§r点击项目名称以修改信息\n'
                        f'§7最后修改者:§6 {list_dic.get(name)["creator"]} §7时间:§6 {list_dic.get(name)["time"]}\n',
                        f'§7项目描述:§6 {list_dic.get(name)["detail"]}\n',
                        f'§7进度描述:§6 {list_dic.get(name)["progress"]}'
                    ),
                    '\n'
                )
                c.append(list_msg)
            server.reply(info, RTextList(*c))
        
        elif args[1] == "reload" or args[1] == "r":
            try:
                read()
                server.say('§b[ToDoList]§a由玩家§d{}§a发起的ToDoList重载成功'.format(info.player))
            except Exception as e:
                server.say('§b[ToDoList]§4由玩家§d{}§4发起的ToDoList重载失败：{}'.format(info.player, e))

    elif len(args) == 3:
        if args[1] == "del" or args[1] == "d":
            name = search(args[2])
            if name:
                del list_dic[name]
                save()
                server.reply(info, f'§b[ToDoList]§a已删除ToDo {name}')
            else:
                server.reply(info, f"§b[ToDoList]§4未查询到 §d{args[2]} §4对应的项目")
            
    elif len(args) == 5:
        if args[1] == "add" or args[1] == "a":
            list_dic[args[2]] = {
                'creator': info.player,
                'time': time.strftime('%Y-%m-%d %H:%M'),
                'detail': args[3],
                'progress': args[4]
            }
            save()
            server.reply(info, f'§b[ToDoList]§a已添加ToDo {args[2]}')

def on_load(server,old):
    server.register_help_message(f'{prefix}', RText('ToDoList').h('点击查看帮助'))
    if not os.path.isfile(config_path):
        save()
    else:
        try:
            read()
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