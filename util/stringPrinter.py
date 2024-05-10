#class StringPrinter:
#  def __init__(self):
#    pass

#  def sprint(self, string, pad, char=' '):
#    print(string.rjust(len(string) + pad), char)

class StringPrinter(DaemonPrinter):
  def __init__(self):
    super().__init__(self)
  def sprint(string, pad, char=' '):
    print(string.rjust(len(string) + pad, char))
  

def sprint(string, pad, char=' '):
  print(string.rjust(len(string) + pad, char))
