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
