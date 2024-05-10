import gdb


class MyBreakpoint:
    def __init__(self):
        self.clean()
        self.main()
        self.rand_init()
        self.read_opts()

    def watchPoint(self, expr, cont=True, definition=None):
        class WatchPoint(gdb.Breakpoint):
            def __init__(self, expr, cont, definition):
                print(isinstance(self, gdb.Breakpoint))
                super().__init__(gdb.BP_WATCHPOINT)
                self.expr = expr
                self.cont = cont
                if definition:
                    self.stop = definition
                else:
                    self.stop = self.definition

            def definition(self):
                if self.definition:
                    print(f"{self.expr}: This is just a test")
                return self.cont

        return WatchPoint(expr, cont, definition)

    def clean(self):
        print("Resetting all breakpoints")
        for bp in gdb.breakpoints():
            bp.delete()

    def main(self):
        class Main(gdb.Breakpoint):
            def stop(self):
                print("Reached main function")

        bp = Main("main")

    def rand_init(self):
        def definition():
            print("Hi from the function")

        self.watchPoint("rand_init", True, definition)

    def read_opts(self):
        class ReadOpts(gdb.Breakpoint):
            def stop(self):
                print("Function: read_opts()")
                frame = gdb.selected_frame()
                argc = frame.read_var("argc")
                argv = frame.read_var("argv")
                print(f"{argc}: arguments, {argv.dereference().string()}")
                # c = gdb.Breakpoint("c", gdb.BP_WATCHPOINT)
                return False

        bp = ReadOpts("read_opts")

    def mark_servers(self):
        pass


myBreakpoint = MyBreakpoint()
