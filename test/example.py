import gdb

class DaemonPrinter(gdb.Command):
  def __init__(self):
    super(DaemonPrinter, self).__init__("pp", gdb.COMMAND_USER)
    self.pad = 0

  def sprint(self, string, pad=0, char=' '):
    print(string.rjust(len(string) + self.pad, char))

  def handleUnion(self, struct, name):
    self.sprint(f"{name} {'{'}", self.pad)
    self.pad = self.pad + 2
    for field in struct.type.fields():
      fname = field.name
      fval = struct[fname]
      _type = field.type
      if fname == "strings":
        print(fval.strings())
      else:
        print("fuck me")
    self.pad = self.pad - 2


  def handleStrings(self, string, name):
    if name == "var":
      i = 0
      arr = []
      while (string+i).dereference() != 0:
        arr.append((string+i).dereference().string())
        i = i + 1 
      print(f"{arr}")
    else:
      print("fuck me")

  def handleInt(self, _int, name):
#    fname = _int.name
    val = _int
    _type = _int.type
    print(_int.type)
    if _type.code == gdb.TYPE_CODE_INT:
      print(f"{name}: {val}")
    elif _type.code == gdb.TYPE_CODE_PTR and val.type.target().code == gdb.TYPE_CODE_INT:
      print(f"{name}: {val.dereference()}")
    else:
      print("fuck me")


  """
  def handleUnion(self, union, name):
    self.sprint(f"{name} {'{'}", self.pad)
    self.pad = self.pad + 2
    self.sprint(f"{dir(union)}", self.pad)
    self.pad = self.pad - 2
    self.sprint("}", self.pad)
  """
  def invoke(self, arg, from_tty):
    if arg:
      args = gdb.string_to_argv(arg)
    else:
      args = gdb.string_to_argv("*dnsmasq_daemon")
    if len(args) != 1:
      print("Usage: pp *dnsmasq_daemon")
      return

    try:
      daemon = gdb.parse_and_eval(args[0])
      self.handleInt(daemon, "val")
    except gdb.error as e:
      print(f"Error {e}")
DaemonPrinter()

# pp *dnsmasq_daemon
