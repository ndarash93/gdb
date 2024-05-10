import gdb


class MyBreakpoint:
    def __init__(self):
        self.clean()
        self.main()
        self.rand_init()
        self.read_opts()

    def watchPoint(self, expr, definition=None):
        class WatchPoint(gdb.Breakpoint):
            def __init__(self, expr, definition):
                print(isinstance(self, gdb.Breakpoint))
                super().__init__(expr, gdb.BP_WATCHPOINT)
                self.expr = expr
                if definition:
                    self.stop = definition
                else:
                    self.stop = self.definition

            def definition(self):
                if self.definition:
                    print(f"{self.expr}: This is just a test")
                return True

        return WatchPoint(expr, definition)

    def myBreakPoint(self, function, definition=None):
        class BreakPoint(gdb.Breakpoint):
            def __init__(self, function, definition):
                print(isinstance(self, gdb.Breakpoint))
                super().__init__(function)
                self.funtion = function
                if definition:
                    self.stop = definition
                else:
                    self.stop = self.definition

            def definition(self):
                print("Generic stop function")
                return True

        return BreakPoint(function, definition)

    def clean(self):
        print("Resetting all breakpoints")
        for bp in gdb.breakpoints():
            bp.delete()

    # ===================================================================================================================== #
    # ===================================================================================================================== #
    # ===================================================================================================================== #
    # ===================================================================================================================== #

    def main(self):
        def stop():
            print("Reached main function")
            return False

        bp = self.myBreakPoint("main", stop)

    def rand_init(self):
        def breakdefinition():
            print("Reached funtion rand_init")
            return False

        def watchPointDefinition():
            frame = gdb.selected_frame()
            watch = frame.read_var("seed")
            print(f"Seed: {watch}")
            return False

        self.myBreakPoint("rand_init", definition=breakdefinition)
        self.watchPoint("seed", definition=watchPointDefinition)

    def read_opts(self):
        def stop():
            print("Function: read_opts()")
            frame = gdb.selected_frame()
            argc = frame.read_var("argc")
            argv = frame.read_var("argv")
            print(f"{argc}: arguments, {argv.dereference().string()}")
            # c = gdb.Breakpoint("c", gdb.BP_WATCHPOINT)
            return False

        bp = self.myBreakPoint("read_opts", definition=stop)

    def mark_servers(self):
        pass


myBreakpoint = MyBreakpoint()
