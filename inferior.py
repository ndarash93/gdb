import gdb
CFLAGS				= -O0 -G

def thread_stopped(event):
  if event.inferior_thread is not None:
    thread = event.inferior_thread
  else:
    thread = gdb.selected_thread()

  inferior = thread.inferior
  
  #1058 poll_resolv -> #1701 reload_servers -> #1800 add_update_server
