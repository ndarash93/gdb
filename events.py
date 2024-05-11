import gdb


def handler(event):
    print("Fuck yourself")


def new_inferior_handle(event):
    print("New")


gdb.events.inferior_call.connect(handler)
gdb.events.new_inferior.connect(new_inferior_handle)
