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
    f"§b{prefix} add <name> (<detail>) (<progress>)": "§r添加/修改<name>项目，可选参数为描述与进度",
}

def get_list(target_tag=""):
    c = ['']

    list_head = RText(f'================== §bToDoList §r==================').c(
        RAction.suggest_command, f'!!td list').h(f'§b!!td list')
    c.append(list_head)

    for name, list_info in fun.list_dic.items():
        tag_list = f''
        for tag in fun.list_dic.get(name)["tags"]:
            if tag not in tag_list and tag != "defult":
                tag_list += f'{tag} '
                if tag == target_tag or target_tag =="":
                    include = True
        if not include:
            continue
        list_msg = RTextList(
                            f'\n- ',
                            RText(f'[×] ', color = RColor.red).c(RAction.suggest_command, f'!!td del {name}')
                                .h(RText(f'Delete', color = RColor.red)),
                            RText(f'[T+] ', color = RColor.green).c(RAction.suggest_command, f'!!td tag add {name} ')
                                .h(RText(f'Add tag', color = RColor.green)),
                                RText(f'[T-] ', color = RColor.green).c(RAction.suggest_command, f'!!td tag del {name} ')
                                .h(RText(f'Delete a tag', color = RColor.red)),
                            RText(f'§b{name}').c(RAction.suggest_command, 
                                                f'!!td add {name} {fun.list_dic.get(name)["detail"][0]} {fun.list_dic.get(name)["progress"]}')
                            .h(
                                f'§r点击项目名以修改信息\n'
                                f'§7最后修改者:§6 {fun.list_dic.get(name)["creator"]} §7时间:§6 {fun.list_dic.get(name)["time"]}',
                                f'\n§7项目类别:§6 {tag_list}' if tag_list != "" else "",
                                f'\n§7项目描述:§6 {fun.list_dic.get(name)["detail"][0]}' if fun.list_dic.get(name)["detail"][0] !="" else "",
                                f'\n§7进度描述:§6 {fun.list_dic.get(name)["progress"]}' if fun.list_dic.get(name)["progress"] !="" else ""
                            )
                        )
        c.append(list_msg)
    return c

def get_tags():
    c = []
    list_head = RText(f'================== §bToDoList-Tags §r==================').c(
        RAction.suggest_command, f'!!td tag').h(f'§b!!td tag')
    tag_list = RTextList()
    tag_list.append(list_head)
    tag_list.append(f'\n')
    for name, list_info in fun.list_dic.items():
        for tag in fun.list_dic.get(name)["tags"]:
            if tag not in c:
                c.append(tag)
    for ctag in c:
        tag_list.append((RText(f'§b<{ctag}> ').c(RAction.suggest_command,f'!!td tag {ctag}'))).h(f'单击以进入对应tag列表')
    return tag_list
    
# def get_taged_list(target):
#     c = ['']
#     list_head = RText(f'================== §b{target} §r==================').c(
#         RAction.suggest_command, f'!!td tag').h(f'§b!!td tag')
#     c.append(list_head)
#     for name, list_info in fun.list_dic.items():
#         for tag in fun.list_dic.get(name)["tags"]:
#             if tag == target:
#                 list_msg = RTextList(
#                                     f'\n- ',
#                                     RText(f'[×] ', color = RColor.red).c(RAction.suggest_command, f'!!td del {name}')
#                                         .h(RText(f'Delete', color = RColor.red)),
#                                     RText(f'§b{name}').c(RAction.suggest_command, 
#                                                         f'!!td add {name} {fun.list_dic.get(name)["detail"][0]} {fun.list_dic.get(name)["progress"]}')
#                                     .h(
#                                         f'§r点击项目名以修改信息\n'
#                                         f'§7最后修改者:§6 {fun.list_dic.get(name)["creator"]} §7时间:§6 {fun.list_dic.get(name)["time"]}',
#                                         f'\n§7项目描述:§6 {fun.list_dic.get(name)["detail"][0]}' if fun.list_dic.get(name)["detail"][0] !="" else "",
#                                         f'\n§7进度描述:§6 {fun.list_dic.get(name)["progress"]}' if fun.list_dic.get(name)["progress"] !="" else ""
#                                     )
#                                 )
#                 c.append(list_msg)
#                 break
#     return c