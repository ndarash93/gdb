import gdb


class MyBreakpoint:
    def __init__(self):
        self.clean()
        self.main()
        self.rand_init()
        self.read_opts()

    def watchPoint(self, expr, cont=True):
        class WatchPoint(gdb.Breakpoint):
            def stop(self):
                print(f"{expr}: Just a test")
                return cont

        return WatchPoint(expr, gdb.BP_WATCHPOINT)

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
        class RandInit(gdb.Breakpoint):
            def __init__(self, expr, watchPoint):
                super().__init__(expr)
                self.watchPoint = watchPoint

            def stop(self):
                print("Function: rand_init()")
                seedWatch = self.watchPoint("seed", cont=False)
                # seedWatch = gdb.Breakpoint("seed", gdb.BP_WATCHPOINT)
                inWatch = gdb.Breakpoint("in", gdb.BP_WATCHPOINT)
                return False

        rand = RandInit("rand_init", self.watchPoint)

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
