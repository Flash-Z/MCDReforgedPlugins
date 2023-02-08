from mcdreforged.api.rtext import *
from todolist.functions import functions as fun

prefix = '!!td'

help_head = """
================== §bToDoList §r==================
以下命令前缀也可只打出首字母，例如(§blist->l§r)
""".format(prefix=prefix)
help_body = {
    f"§b{prefix}": "§r显示本帮助信息",
    f"§b{prefix} list": "§r显示ToDoList",
    f"§b{prefix} del <name>": "§r删除<name>",
    f"§b{prefix} reload": "§r重载插件配置",
    f"§b{prefix} add <name> <detail> <progress>": "§r添加/修改名为<name>的项目，可选参数为描述与进度",
}

def get_list():
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
                                f'\n§7进度描述:§6 {fun.list_dic.get(name)["progress"]}' if fun.list_dic.get(name)["progress"] !="" else ""
                            )
                        )
        c.append(list_msg)
    return c