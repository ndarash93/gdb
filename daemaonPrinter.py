import sys
sys.dont_write_bytecode = True
#sys.modules.clear()

import importlib
import gdb
import sys
import os

class DaemonPrinter(gdb.Command):
  def __init__(self):
    super(DaemonPrinter, self).__init__("pp", gdb.COMMAND_USER)
    self.pad = 0

  def sprint(self, string, pad=0, char=' '):
    print(string.rjust(len(string) + self.pad, char))

  def handleField(self, name, val, _type, raw):
    self.incPad()
    name = name.split('.')[-1]
    if val.type.code == gdb.TYPE_CODE_PTR and str(val.type.target()) == "char":
      self.handleString(name, val)
    elif _type.code == gdb.TYPE_CODE_INT or (_type.code == gdb.TYPE_CODE_PTR and _type.target().code == gdb.TYPE_CODE_INT):
      self.handleInt(val, name)
    elif name == "resolv_files":
      self.handleResolvc(val, name)
    elif name == "options":
      self.handleOptions(val)
    elif name == "default_resolv":
      self.handleResolvc(val, name)
    elif name == "mxnames":
      self.handleMxSrvRecord(val, name)
    elif name == "naptr":
      self.handleNaptr(val, name)
    elif name == "txt" or name == "rr":
      self.handleTxtRecord(val, name)
    elif name == "ptr":
      self.handlePtrRecord(val, name)
    elif name == "host_records" or name == "host_records_tail":
      self.handleHostRecord(val, name) #TODO
    elif name == "cnames":
      self.handleCName(val, name)
    elif name == "auth_zones":
      self.handleAuthZone(val, name)
    elif name == "int_names":
      self.handleInterfaceName(val, name)
    elif name == "add_subnet4" or name == "add_subnet6":
      self.handleSubNet(val, name)
    elif name in ['authinterface', 'if_names', 'if_addrs', 'if_except', 'dhcp_except', 'auth_peers', 'tftp_interfaces']:
      self.handleIName(val, name)
    elif name == "secondary_forward_server":
      self.handleNameList(val, name)
    elif name in ["group_set", " osport"]:
      self.handleInt(val, name)
    elif name == "cond_domain" or name == "synth_domains":
      self.handleCondDomain(val, name)
    elif name == "bogus_addr" or name == "ignore_addr":
      self.handleBogusAddr(val, name)
    elif name in ["servers", "servers_tail", "local_domains", "serverarray", "srv_save"]:
      self.handleServer(val, name)
    elif name == "no_rebind":
      self.handleRebindDomain(val, name)
    elif name in ["ipsets", "nftsets"]:
      self.handleIpsets(val, name)
    elif name == "allowlists":
      self.handleAllowList(val, name)
    elif name in ["addn_hosts", "dhcp_hosts_file", "dhcp_opts_file", "dynamic_dirs"]:
      self.handleHostsFile(val, name)
    elif name in ["dhcp", "dhcp6"]:
      self.handleDhcpContext(val, name)
    elif name == "ra_interfaces":
      self.handleRaInterface(val, name)
    elif name == "dhcp_conf":
      self.handleDhcpConfig(val, name)
    elif name in ["dhcp_opts", "dhcp_match", "dhcp_opts6", "dhcp_match6"]:
      self.handleDhcpOpt(val, name)
    elif name == "dhcp_name_match":
      self.handleDhcpMatchName(val, name)
    elif name == "dhcp_pxe_vendors":
      self.handleDhcpPxeVendor(val, name)
    elif name == "dhcp_vendors":
      self.handleDhcpVendor(val, name)
    elif name == "dhcp_mac":
      self.handleDhcpMac(val, name)
    elif name == "dhcp_boot":
      self.handleDhcpBoot(val, name)
    elif name == "pxe_service":
      self.handlePxeService(val, name)
    elif name == "tag_if":
      self.handleTagIf(val, name)
    elif name in ["override_relays", "interface_addrs"]:
      self.handleAddrList(val, name)
    elif name in ["relay4", "relay6"]:
      self.handleDhcpRelay(val, name)
    elif name == "delay_conf":
      self.handleDelayConfig(val, name)
    elif name in ["dhcp_ignore", "dhcp_ignore_names", "dhcp_gen_names", "force_broadcast", "bootp_dynamic"]:
      self.handleDhcpNetidList(val, name)
    elif name == "doctors":
      self.handleDoctor(val, name)
    elif name == "if_prefix":
      self.handleTftpPrefix(val, name)
    elif name == "frec_list":
      self.handleFrec(val, name)
    elif name == "free_frec_src":
      self.handleFrecSrc(val, name)
    elif name == "sfds":
      self.handleServerFd(val, name)
    elif name == "randomsocks":
      self.handleRandFd(val, name)
    elif name == "log_source_addr":
      self.handleMySockAddr(val, name)
    elif name in ["dhcp_packet", "outpacket"]:
      self.handleIovec(val, name)
    elif name == "bridges":
      self.handleDhcpBridge(val, name)
    elif name == "shared_networks":
      self.handleSharedNetwork(val, name)
    elif name == "free_snoops":
      self.handleSnoopRecord(val, name)
    self.decPad()
    return "TODO"

  def handleString(self, name, string):
    if string != 0:
      self.sprint(f"{name}: \"{string.string()}\"")
    else:
      self.sprint(f"{name}: NULL")

  def handleStringArr(strings, name):
    arr = []
    i = 0
    while (strings+1).dereference() != 0:
      arr.append((strings+1).dereference().string())
    self.sprint(f"{arr}", self.pad)

  def handleInt(self, _int, name):
    if _int.type.code == gdb.TYPE_CODE_INT:
      self.sprint(f"{name}: {str(_int)}", self.pad)
    elif _int.type.code == gdb.TYPE_CODE_PTR and _int != 0:
      self.handleInt(_int.dereference())
    elif _int.type.code == gdb.TYPE_CODE_PTR and _int == 0:
      self.sprint(f"{name}: NULL", self.pad)
    else:
      self.sprint(f"{name}: Error", self.pad)

  def incPad(self):
    self.pad = self.pad + 2

  def decPad(self):
    self.pad = self.pad - 2

  # TODO Fix
  def handleOptions(self, val):
    print("Options: ".rjust(len("Options: ") + self.pad, ' '), end='')
    for i in range(3):
      print(f"{val[i]} ",end='')
    print()

  # Needs to be updated
  def handleResolvc(self, res, name):
    if res.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in res.type.fields():
        fname = field.name
        val = res[fname]
        _type = field.type 
        if _type.code == gdb.TYPE_CODE_PTR and _type.target().code == gdb.TYPE_CODE_STRUCT and fname == "next":
          self.handleResolvc(val, fname)
        elif _type.code == gdb.TYPE_CODE_PTR and str(_type.target()) == "char":
          self.handleString(fname, val)
        elif _type.code == gdb.TYPE_CODE_INT:
          self.sprint(f"{fname}: {val}")
      self.decPad()
      self.sprint("}")
    elif res.type.code == gdb.TYPE_CODE_PTR and res != 0:
      self.handleResolvc(res.dereference(), name)
    elif res.type.code == gdb.TYPE_CODE_PTR and res == 0:
      self.sprint("NULL")
    else:
      self.sprint("Error")

  def handleNaptr(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_PTR and str(_type.target()) == "char":
          self.handleString(fname, val)
        else:
          self.handleString(fname, 0)
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error") 

  def handleMxSrvRecord(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_PTR and str(_type.target()) == "char":
          self.handleString(fname, val)
        elif _type.code == gdb.TYPE_CODE_INT:
          self.handleInt(fname, val)
        elif _type.code == gdb.TYPE_CODE_PTR and _type.target().code == gdb.TYPE_CODE_STRUCT and name == "next":
          self.handleMxSrvRecord(val, fname)
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleTxtRecord(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_PTR and str(_type.target()) == "char":
          self.handleString(fname, val)
        #elif _type.code == gdb.TYPE_CODE_INT and val.type.sizeof == 2:
          #sprint(f"{fname}: {int(val)}", self.pad)
        elif _type.code == gdb.TYPE_CODE_INT:
          self.sprint(f"{fname}: {int(val)}")
        elif _type.code == gdb.TYPE_CODE_PTR and _type.target().code == gdb.TYPE_CODE_STRUCT and fname == "next" and val != 0:
          self.handleTxtRecord(val, fname)
        else:
          self.sprint(f"{fname}: NULL")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handlePtrRecord(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_PTR and str(_type.target()) == "char":
          self.handleString(fname, val)
        elif _type.code == gdb.TYPE_CODE_PTR and _type.target().code == gdb.TYPE_CODE_STRUCT and fname == "next" and val != 0:
          self.handleTxtRecord(val, fname)
        else:
          self.sprint(f"{fname}: NULL")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint("Error")

  def handleHostRecord(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_INT:
          self.sprint(f"{fname}: {val}")
        elif _type.code == gdb.TYPE_CODE_PTR and fname == "names":
          self.handleNameList(val, fname)
        elif fname == "addr":
          self.handleInAddr(val, fname)
        elif fname == "in6_addr":
          self.handleIn6Addr(val, fname)
        elif fname == "next":
          self.handleHostRecord(val, fname)
        else:
          self.sprint("Error") 
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f'{name}: NULL')
    else:
      self.sprint(f"{name}: Error")

  def handleNameList(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_PTR and val.type.target() == "char":
          self.handleStr(fname, val)
        elif fname == "next":
          self.handleNameList(val, fname)
        else:
          self.sprint(f"{fname}: NULL")
      self.decPad()
      sprint("}", self.pad)
    else:
      self.sprint(f"{name}: Error")

  # TODO This struct should just be an int
  def handleInAddr(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        self.sprint(f"{fname}: {val} ({_type})")
      self.decPad()
      self.sprint("}")
    else:
      self.sprint(f"{name}: Error")
   

  def handleIn6Addr(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        self.sprint(f"{fname}: {val} ({_type})")
      self.decPad()
      self.sprint("}")
    else:
      self.sprint(f"{name}: Error")


  def handleCrec(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "next" or fname == "prev" or fname == "hash_next":
          self.handleCrec(val, fname)
        elif fname == "addr":
          self.handleAllAddr(val, fname)
        elif fname == "ttd" or fname == "uid" or fname == "flags":
          self.sprint(f"{fname}: {val}")
        elif fname == "name": #if flag & F_BIGNAME then BNAME elif flag & F_NAMEP then namep else sname
          for _field in val.type.fields():
            _fname = _field.name
            _val = val[_fname]
            __type = _field.type
            if _fname == "sname":
              self.handleString(_fname, _val)
            elif _fname == "bname":
              self.handleBigname(_val, _fname)
            elif _fname == "namep":
              self.handleString(_fname, _val)
            else:
              self.sprint(f"{_fname}: Error")
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleCrec(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  ## Broken
  """
  def handleBigname(self, union, name):
    if union.type.code == gdb.TYPE_CODE_UNION:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in union.type.fields():
        fname = field.name
        val = union[fname]
        _type = field.type
        if fname == "name":
          self.handleString(fname, val)
        elif fname == "name":
          self.handleBigname(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif union.type.code == gdb.TYPE_CODE_PTR and union != 0:
      self.handleBigname(union.dereference(), name)
    elif union.type.code == gdb.TYPE_CODE_PTR and union == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")
  """

  def handleBigname(self, union, name):
    print("broken for now")

  def handleCName(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_INT:
          self.sprint(f"{fname}: {val}")
        elif val.type.code == gdb.TYPE_CODE_PTR and str(val.type.target()) == "char":
          self.handleString(fname, val)
        elif fname == "name" or fname == "targetp":
          self.handleCName(val, fname)
        else:
          self.sprint(f"{name} Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleAuthZone(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad() 
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if val.type.code == gdb.TYPE_CODE_PTR and str(val.type.target()) == "char":
          self.handleString(fname, val)
        elif fname == "interface_names":
          self.handleAuthNameList(val, fname)
        elif fname == "subnet" or fname == "exclude":
          self.handleAllAddr(val, fname)
        elif _type == gdb.TYPE_CODE_PTR and fname == "next" and val != 0:
          self.handleAuthZone(val, fname)
        elif _type == gdb.TYPE_CODE_PTR and fname == "next" and val == 0:
          self.sprint(f"{fname}: NULL")
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")
          

  def handleAddrList(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name}{'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if val.type.code == gdb.TYPE_CODE_UNION and fname == "addr":
          self.handleAllAddr(val, fname)
        elif fname == "flags" or fname == "prefixlen":
          self.sprint(f"{fname}: {val}")
        elif _type == gdb.TYPE_CODE_PTR and fname == "next" and val != 0:
          self.handleAddrList(val, fname)
        elif _type == gdb.TYPE_CODE_PTR and fname == "next" and val == 0:
          self.sprint(f"{fname}: NULL")
        else:
          self.sprint(f"{fname}: Error")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")
      
  
  def handleAuthNameList(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.derefenece().type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type 
        if val.type.code == gdb.TYPE_CODE_PTR and str(val.type.target()) == "char":
          self.handleString(fname, val)
        elif _type == gdb.TYPE_CODE_INT:
          self.sprint(f"{fname}: {val}")   
        elif fname == "next":
          self.handleAuthNameList(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.sprint(f"{'}'}")
      self.decPad()
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  ## Needs to be fixed once we learn how we want to handle unions
  """
  def handleAllAddr(self, union, name):
    if union.type.code == gdb.TYPE_CODE_UNION:
      self.sprint(f"{name}{'{'}}")
      self.incPad()
      for field in union.type.fields():
        fname = field.name
        val = union[fname]
        _type = field.type
        self.sprint(f"{fname}: {val}")
    else:  
      self.sprint(f"{name}: Error")
    print("This is just a test")
    """

  def handleAllAddr(self, union, name):
    print("Broken for now")

  def handleInterfaceName(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.dereference().type.fields():
        fname = field.name
        val = stuct[fname]
        _type = field.type
        if _type.code == gdb.TYPE_CODE_PTR and str(_type.target()) == "char":
          self.hanleString(fname, val)
        elif _type.code == gdb.TYPE_CODE_INT and fname == "flags":
          self.sprint(f"{fname}: {val}")
        elif _type.code == gdb.TYPE_CODE_STRUCT and fname == "proto4":
          self.handleInAddr(val, fname)
        elif _type.code == gdb.TYPE_CODE_STRUCT and fname == "proto6":
          self.handleIn6Addr(val, fname)
        elif _type.code == gdb.TYPE_CODE_PTR and fanme == "addr":
          self.handleAddrList(val, fname) 
        elif _type.code == gdb.TYPE_CODE_PTR and fanme == "next":
          self.handleInterfaceName(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  # Use this as template funxtion
  def handleSubNet(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "addr":
          self.handleMySockAddr(val, fname)
        elif fname == "addr_used" or fname == "mask":
          self.sprint(f"{fname}: {hex(val)}")
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleCrec(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleIName(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "name":
          self.handleString(fname, val)
        elif fname == "addr":
          self.handleMySockAddr(val, fname)
        elif fname == "used":
          self.sprint(f"{fname}: {hex(val)}")
        elif fname == "next":
          self.handleIName(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleIName(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  # Union issue
  def handleMySockAddr(self, union, name):
    print("Broken for now")

  def handleSockAddr(self, struct, name):
    print("Testing struct sockaddr")

  def handleCondDomain(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["domain", "prefix", "interface"]:
          self.handleString(fname, val)
        elif fname == "al":
          self.handleAddrList(val, fname)
        elif fname == "start" or fname == "end":
          self.handleInAddr(val, fname)
        elif fname == "start6" or fname == "end6":
          self.handleIn6Addr(val, fname)
        elif fname in ["is6", "indexed", "prefixlen"]:
          self.handleInt(val, name)
        elif fname == "next":
          self.handleCondDomain(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleCondDomain(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleBogusAddr(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["is6", "prefix"]:
          self.handleInt(val, fname)
        elif fname == "addr":
          self.handleAllAddr(val, fname)
        elif fname == "next":
          self.handleBogusAddr(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleBogusAddr(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleServer(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["flags", "domain_len"]:
          self.sprint(f"{fname}: {hex(val)}", self.pad)
        elif fname in ["serial", "arrayposn", "last_server", "ifindex", "tcpfd", "edns_pktsz", "pktz_reduced", "queries", "failed_queries", "forwardtime", "forwardcount", "uid"]:
          self.handleInt(val, fname)
        elif fname in ["domain", "interface"]:
          self.handleString(fname, val)
        elif fname in ["addr", "source_addr"]:
          self.handleMySockAddr(val, fname)
        elif fname == "next":
          self.handleServer(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleServer(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")
  
  def handleRebindDomain(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "domain":
          self.handleString(name, val)
        elif fname == "next":
          self.handleRebindDomain(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleRebindDomain(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleIpsets(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "sets":
          self.handleStringArr(name, val)
        elif fname == "domain":
          self.handleString(name, val)
        elif fname == "next":
          self.handleIpsets(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleIpsets(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleAllowList(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["mark", "mask"]:
          self.sprint(f"{fname}: {hex(val)}", self.pad)
        elif fname == "patterns":
          self.handleStringArr(name, val)
        elif fname == "next":
          self.handleAllowList(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleAllowList(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleHostsFile(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["wd", "index"]:
          self.sprint(f"{fname}: {val}", self.pad)
        elif fname == "flags":
          self.sprint(f"{fname}: {hex(val)}", self.pad)
        elif fname == "fname":
          self.handleString(fname, val)
        elif fname == "next":
          self.handleHostsFile(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleHostsFile(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpContext(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["lease_time", "addr_epoch", "prefix", "if_index", "valid", "preferred", "saved_valid", "ra_time", "ra_short_period_start", "address_lost_time"]:
          self.sprint(f"{fname}: {val}", self.pad)
        elif fname == "flags":
          self.sprint(f"{fname}: {hex(val)}", self.pad)
        elif fname in ["netmask", "broadcast", "local", "router", "start", "end"]:
          self.handleInAddr(val, fname)
        elif fname in ["start6", "end6", "local6"]:
          self.handleIn6Addr(val, fname)
        elif fname == "current":
          self.sprint(f"{fname}: {val}", self.pad) # Update to val.address if this is an address
        elif fname in ["netid", "filter"]:
          self.handleDhcpNetid(val, fname)
        elif fname == "next":
          self.handleDhcpContext(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpContext(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  
  def handleDhcpNetid(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "net":
          self.handleString(val, fname)
        elif fname == "next":
          self.handleDhcpNetid(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpNetid(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

#TODO
  def handleDhcpNetidList(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "list":
          self.handleDhcpNetid(val, fname)
        elif fname == "next":
          self.handleDhcpNetidList(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpNetidList(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")



  def handleRaInterface(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["name",  "mtu_name"]:
          self.handleString(val, fname)
        elif fname in ["interval", "lifetime", "prio", "mtu"]:
          self.handleInt(val, fname)
        elif fname == "next":
          self.handleRaInterface(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleRaInterface(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpConfig(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "flags":
          self.sprint(f"{fname}: {hex(val)}", self.pad)
        elif fname in ["clid_len", "decline_time", "lease_time"]:
          self.handleInt(val, fname)
        elif fname == "netid":
          self.handleDhcpNetidList(val, fname)
        elif fname == "filter":
          self.handleDhcpNetid(val, fname)
        elif fname == "addr6":
          self.handleAddrList(val, fname)
        elif fname == "addr":
          self.handleInAddr(val, fname)
        elif fname == "hwaddr":
          self.handleHwaddrConfig(val, fname)
        elif fname == "next":
          self.handleDhcpConfig(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpConfig(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleHwaddrConfig(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["hwaddr_len", "hwaddr_type", "wildcard_mask"]:
          self.handleInt(val, fname)
        elif fname == "hwaddr":
          self.handleString(fname, val)
        elif fname == "next":
          self.handleHwaddrConfig(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleHwaddrConfig(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpOpt(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["opt", "len"]:
          self.handleInt(val, fname)
        elif fname == "flags":
          self.sprint(f"{fname}: {hex(val)}", self.pad)
        elif fname == "u":
          self.sprint(f"{fname}: {hex(val)}", self.pad) # TODO this is not ideal but we still dont know how to handle unions
        elif fname == "netid":
          self.handleDhcpNetid(val, fname)
        elif fname == "next":
          self.handleDhcpOpt(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpOpt(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpMatchName(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "name":
          self.handleString(fname, val)
        elif fname == "wildcard":
          self.handleInt(val, fname)
        elif fname == "netid":
          self.handleDhcpNetid(val, fname)
        elif fname == "next":
          self.handleDhcpMatchName(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpMatchName(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpPxeVendor(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "data":
          self.handleString(fname, val)
        elif fname == "next":
          self.handleDhcpPxeVendor(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpPxeVendor(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpVendor(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "data":
          self.handleString(fname, val)
        elif fname in ["len", "match_type", "enterprise"]:
          self.handleInt(val, fname)
        elif fname == "netid":
          self.handleNetid(val, fname)
        elif fname == "next":
          self.handleDhcpVendor(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpVendor(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpMac(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "mask":
          self.sprint(f"{fname}: {hex(val)}", self.pad)
        elif fname in ["hwaddr_len", "hwaddr_type"]:
          self.handleInt(val, fname)
        elif fname == "hwaddr":
          self.handleString(fname, val)
        elif fname == "netid":
          self.handleNetid(val, fname)
        elif fname == "next":
          self.handleDhcpMac(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpMac(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpBoot(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["file", "sname", "tftp_sname"]:
          self.handleString(fname, val)
        elif fname == "next_server":
          self.handleInAddr(val, fname)
        elif fname == "netid":
          self.handleNetid(val, fname)
        elif fname == "next":
          self.handleDhcpBoot(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpBoot(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handlePxeService(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["CSA", "type"]:
          self.sprint(f"{fname}: {int(val)}", self.pad)
        elif fname in ["menu", "basename", "sname"]:
          self.handleString(fname, val)
        elif fname == "server":
          self.handleInAddr(val, fname)
        elif fname == "netid":
          self.handleNetid(val, fname)
        elif fname == "next":
          self.handlePxeService(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handlePxeService(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleTagIf(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "set":
          self.handleDhcpNetidList(val, fname)
        elif fname == "tag":
          self.handleDhcpNetid(val, fname)
        elif fname == "next":
          self.handleTagIf(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleTagIf(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpRelay(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["local", "server"]:
          self.handleAllAddr(val, fname)
        elif fname == "interface":
          self.handleString(fname, val)
        elif fname in ["iface_index", "port"]:
          self.handleInt(val, fname)
        elif fname == "snoop_records":
          self.handleSnoopRecord(val, fname)
        elif fname == "next":
          self.handleDhcpRelay(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpRelay(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleSnoopRecord(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["client", "prefix"]:
          self.handleIn6Addr(val, fname)
        elif fname == "prefix_len":
          self.handleInt(val, fname)
        elif fname == "next":
          self.handleSnoopRecord(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleSnoopRecord(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDelayConfig(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "delay":
          self.handleInt(val, fname)
        elif fname == "netid":
          self.handleDhcpNetid(val, fname)
        elif fname == "next":
          self.handleDelayConfig(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDelayConfig(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDoctor(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["in", "end", "out", "mask"]:
          self.handleInAddr(val, fname)
        elif fname == "next":
          self.handleDoctor(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDoctor(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleTftpPrefix(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["interface", "prefix"]:
          self.handleString(fname, val)
        elif fname == "missing":
          self.handleInt(val, fname)
        elif fname == "next":
          self.handleTftpPrefix(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleTftpPrefix(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleFrec(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "frec_source":
          self.handleFrecSrc(val, fname)
        elif fname == "sentto":
          self.handleServer(val, fname)
        elif fname == "rfds":
          self.handleRandFdList(val, fname)
        elif fname in ["new_id", "forwardall", "time"]:
          self.handleInt(val, fname)
        elif fname == "hash":
          self.handleString(fname, val)
        elif fname == "next":
          self.handleFrec(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleFrecSrc(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleFrecSrc(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "source":
          self.handleMySockAddr(val, fname)
        elif fname == "dest":
          self.handleAllAddr(val, fname)
        elif fname in ["iface", "log_id", "fd", "orig_id"]:
          self.handleInt(val, fname)
        elif fname == "next":
          self.handleFrecSrc(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleFrecSrc(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleServerFd(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["fd", "ifindex", "used", "preallocated"]:
          self.handleInt(val, fname)
        elif fname == "source_addr":
          self.handleMySockAddr(val, fname)
        elif fname == "interface":
          self.handleString(fname, val)
        elif fname == "next":
          self.handleServerFd(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleServerFd(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleIrec(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "addr":
          self.handleMySockAddr(val, fname)
        elif fname == "netmask":
          self.handleInAddr(val, fname)
        elif fname in ["tftp_ok", "dhcp_ok", "mtu", "done", "warned", "dad", "dns_auth", "index", "multicast_done", "found", "label"]:
          self.handleInt(val, fname)
        elif fname == "name":
          self.handleString(fname, val)
        elif fname == "next":
          self.handleIrec(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleIrec(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleListener(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["fd", "tcpfd", "tftpfd", "used"]:
          self.handleInt(val, fname)
        elif fname == "addr":
          self.handleMySockAddr(val, fname)
        elif fname == "iface":
          self.handleIrec(val, fname)
        elif fname == "next":
          self.handleListener(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleListener(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleRandFd(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "serv":
          self.handleServer(val, fname)
        elif fname in ["fd", "refcount"]:
          self.handleInt(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleRandFd(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleRandFdList(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "rfd":
          self.handleRandFd(val, fname)
        elif fname == "next":
          self.handleRandFdList(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleRandFdList(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleIovec(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname in ["iov_base", "iov_len"]:
          self.handleInt(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleIovec(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handlePingResult(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "addr":
          self.handleInAddr(val, fname)
        elif fname in ["time", "hash"]:
          self.handleInt(val, fname)
        elif fname == "next":
          self.handlePingResult(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handlePingResult(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleDhcpBridge(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "iface":
          self.handleString(fname, val)
        elif fname in ["next", "alias"]:
          self.handleDhcpBridge(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleDhcpBridge(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")

  def handleSharedNetwork(self, struct, name):
    if struct.type.code == gdb.TYPE_CODE_STRUCT:
      self.sprint(f"{name} {'{'}")
      self.incPad()
      for field in struct.type.fields():
        fname = field.name
        val = struct[fname]
        _type = field.type
        if fname == "if_index":
          self.handleInt(val, fname)
        elif fname in ["match_addr", "shared_addr"]:
          self.handleInAddr(val, fname)
        elif fname in ["match_addr6", "shared_addr6"]:
          self.handleIn6Addr(val, fname)
        elif fname == "next":
          self.handleSharedNetwork(val, fname)
        else:
          self.sprint(f"{fname}: Error")
      self.decPad()
      self.sprint("}")
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct != 0:
      self.handleSharedNetwork(struct.dereference(), name)
    elif struct.type.code == gdb.TYPE_CODE_PTR and struct == 0:
      self.sprint(f"{name}: NULL")
    else:
      self.sprint(f"{name}: Error")


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
        if args[0] == "*dnsmasq_daemon":
          print(f"{arg} {'{'}")
          for field in daemon.type.fields():
            fname = field.name
            fval = daemon[fname]
            ftype = field.type
            self.handleField(str(fname), fval, ftype, field)
          print("}")
        else:
          self.handleField(str(arg), daemon, daemon.type, daemon)
      except gdb.error as e:
        print(f"Error {e}")

DaemonPrinter()

# pp *dnsmasq_daemon
