class DaemonPrinter:
  def __init__(self, val):
    self.val = val

  def handleField(self, field):
    field_value = self.val[field.name]
    field_name = str(field.name)
    field_type = str(field.type)

    if field_name == "options":
      #for i in  
      return selfrval['options']
    
    #if field_name == "last_resolv":
      #for i in 
      #return str(type(field_value))
    return field_type

  def to_string(self):
    output = "Daemon {\n"
    #for field in self.val.type.fields():
      #output += f"{field.name} = {self.handleField(field)}\n"
    for i in self.val.type:
      output += f"{i}, {self.val[i]}\n"

    output += "}"
    return output

def my_pp_func(val):
  return DaemonPrinter(val)

gdb.pretty_printers.append(my_pp_func)
