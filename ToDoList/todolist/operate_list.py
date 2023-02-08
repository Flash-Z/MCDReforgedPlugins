import time
from mcdreforged.api.rtext import *
from mcdreforged.api.decorator import new_thread

from todolist.UI import *
from todolist.functions import functions as fun

@new_thread("ToDoList_op_list")
def operate_list(server, info, args):
    if len(args) == 1:
        head = [help_head]
        body = [RText(f'{k} {v}\n').c(
            RAction.suggest_command, k.replace('§b', '')).h(v)
                for k, v in help_body.items()]
        server.reply(info, RTextList(*(head + body)))

    if args[1] == "add" or args[1] == "a":
        fun.list_dic[args[2]] = {
            'creator': info.player,
            'time': time.strftime('%Y-%m-%d %H:%M'),
            'tags':['defult'],
            'detail': [args[3] if len(args) == 4 else ''],
            'progress': args[4] if len(args) == 5 else ''
        }
        fun.save()
        server.reply(info, f'§b[ToDoList]§a已添加ToDo {args[2]}')
    
    elif len(args) == 2:
        if args[1] == "list" or args[1] == "l":
            c = ['']

            list_head = RText(f'================== §bToDoList §r==================').c(
                RAction.suggest_command, f'!!td list').h(f'§b!!td list')
            c.append(list_head)

            for name, list_info in fun.list_dic.items():
                list_msg = RTextList(
                    f'\n- ',
                    RText(f'[×] ', color = RColor.red).c(RAction.suggest_command, f'!!td del {name}')
                        .h(RText(f'Delete', color = RColor.red)),
                    RText(f'§b{name}').c(RAction.suggest_command, 
                                         f'!!td add {name} {fun.list_dic.get(name)["detail"][0]} {fun.list_dic.get(name)["progress"]}')
                    .h(
                        f'§r点击项目名以修改信息\n'
                        f'§7最后修改者:§6 {fun.list_dic.get(name)["creator"]} §7时间:§6 {fun.list_dic.get(name)["time"]}',
                        # f'\n§7项目类别:§6 {fun.list_dic.get(name)["tags"]}',
                        f'\n§7项目描述:§6 {fun.list_dic.get(name)["detail"][0]}' if fun.list_dic.get(name)["detail"][0] !="" else "",
                        f'\n§7进度描述:§6 {fun.list_dic.get(name)["progress"]}' if fun.list_dic.get(name)["detail"][0] !="" else ""
                    )
                )
                c.append(list_msg)
            server.reply(info, RTextList(*c))
        
        elif args[1] == "reload" or args[1] == "r":
            try:
                fun.read()
                server.say('§b[ToDoList]§a由玩家§d{}§a发起的ToDoList重载成功'.format(info.player))
            except Exception as e:
                server.say('§b[ToDoList]§4由玩家§d{}§4发起的ToDoList重载失败：{}'.format(info.player, e))

    elif len(args) == 3:
        if args[1] == "del" or args[1] == "d":
            name = fun.search(args[2])
            if name:
                del fun.list_dic[name]
                fun.save()
                server.reply(info, f'§b[ToDoList]§a已删除ToDo {name}')
            else:
                server.reply(info, f"§b[ToDoList]§4未查询到 §d{args[2]} §4对应的项目")