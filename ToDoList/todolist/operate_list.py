import time
from mcdreforged.api.rtext import *
from mcdreforged.api.decorator import new_thread

from todolist.UI import *
from todolist.functions import functions as fun

@new_thread("ToDoList_op_list")
def operate_list(server, info, args):
    if args[1] == "test":
        server.reply(info, get_simple_taged_list("defult"))
    if len(args) == 1:
        head = [help_head]
        body = [RText(f'{k} {v}\n').c(
            RAction.suggest_command, k.replace('§b', '')).h(v)
                for k, v in help_body.items()]
        server.reply(info, RTextList(*(head + body)))

    elif args[1] == "add" or args[1] == "a":
        if args[2] in fun.list_dic:
            tag_list = []
            for tag in fun.list_dic.get(name)["tags"]:
                if tag not in tag_list:
                    tag_list.append(tag)
        else: tag_list = ['defult']
        fun.list_dic[args[2]] = {
            'creator': info.player,
            'time': time.strftime('%Y-%m-%d %H:%M'),
            'tags':tag_list,
            'detail': [args[3] if len(args) == 4 else ''],
            'progress': args[4] if len(args) == 5 else ''
        }
        fun.save()
        server.reply(info, f'§b[ToDoList]§a已添加ToDo {args[2]}')
    
    elif args[1] == "tag" or args[1] == "t":
        if len(args) == 2:
            server.reply(info, get_tags())
        elif len(args) == 3:
            server.reply(info, RTextList(*get_taged_list(args[2])))
        elif len(args) == 5: 
            if args[2] == "add" or args[2] == "a": # !!td tag add <name> <tag>
                if args[4] not in fun.list_dic[args[3]]:
                    fun.list_dic[args[3]]["tags"].append(args[4])
                    fun.save()
                    server.reply(info, f'§b[ToDoList]§a已添加ToDo {args[2]}')
            if args[2] == "del" or args[2] == "d": # !!td tag del <name> <tag>
                new_tag = []
                temp_tag = fun.list_dic[args[3]]["tags"]
                for old_tag in temp_tag:
                    if old_tag != args[4]:
                        new_tag.append(old_tag)
                fun.list_dic[args[3]]["tags"] = new_tag
                fun.save()
                server.reply(info, f'§b[ToDoList]§a已添加ToDo {args[2]}')
            
            
    elif len(args) == 2:
        if args[1] == "list" or args[1] == "l":
            server.reply(info, RTextList(*get_list()))
        
        elif args[1] == "reload" or args[1] == "r":
            try:
                fun.read()
                server.say('§b[ToDoList]§a由玩家§r{}§a发起的ToDoList重载成功'.format(info.player))
            except Exception as e:
                server.say('§b[ToDoList]§4由玩家§r{}§4发起的ToDoList重载失败：{}'.format(info.player, e))

    elif len(args) == 3:
        if args[1] == "del" or args[1] == "d":
            name = fun.search(args[2])
            if name:
                del fun.list_dic[name]
                fun.save()
                server.reply(info, f'§b[ToDoList]§a已删除ToDo {name}')
            else:
                server.reply(info, f"§b[ToDoList]§4未查询到 §d{args[2]} §4对应的项目")