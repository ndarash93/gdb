import gdb


class MyBreakpoint:
    def __init__(self):
        self.clean()
        self.main()
        # self.rand_init()
        # self.read_opts()
        self.netlink_init()

    def myWatchPoint(self, expr, definition=None):
        class WatchPoint(gdb.Breakpoint):
            def __init__(self, expr, definition):
                if not isinstance(self, gdb.Breakpoint):
                    print("Something weird")
                super().__init__(expr, gdb.BP_WATCHPOINT)
                self.expr = expr
                if definition:
                    self.stop = definition
                else:
                    self.stop = self.definition

            def definition(self):
                return True

        return WatchPoint(expr, definition)

    def myBreakPoint(self, function, definition=None):
        class BreakPoint(gdb.Breakpoint):
            def __init__(self, function, definition):
                if not isinstance(self, gdb.Breakpoint):
                    print("Something weird")
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

    def myFinishPoint(self, frame, definition=None):
        class FinishPoint(gdb.FinishBreakpoint):
            def __init__(self, frame, definition):
                if not isinstance(self, gdb.FinishBreakpoint):
                    print("Something weird")
                super().__init__(frame)
                # print(frame)
                self.frame = frame
                if definition:
                    self.stop = definition
                else:
                    self.stop = self.definition

            def definition(self):
                print("Generic Finish")
                return True

            def out_of_scope():
                print("Abnormal Finish")

        return FinishPoint(frame, definition)

    def clean(self):
        print("Resetting all breakpoints")
        for bp in gdb.breakpoints():
            bp.delete()

    # =========================================================================================== #
    # =========================================================================================== #
    # =========================================================================================== #
    # =========================================================================================== #

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
            print("Test")
            frame = gdb.selected_frame()
            watch = frame.read_var("seed")
            print(f"Seed: {watch}")
            return False

        self.myBreakPoint("rand_init", definition=breakdefinition)

    def read_opts(self):
        def stopWatch():
            frame = gdb.selected_frame()
            option = frame.read_var("option")
            print(f"Option: {option}")
            return False

        def stop():
            print("Function: read_opts()")
            frame = gdb.selected_frame()
            argc = frame.read_var("argc")
            argv = frame.read_var("argv")
            print(f"{argc}: arguments, {argv.dereference().string()}")
            watch = self.myWatchPoint("option", definition=stopWatch)
            return False

        bp = self.myBreakPoint("read_opts", definition=stop)

    def mark_servers(self):
        pass

    def netlink_init(self):
        def stopFinish():
            print("Stop function called")
            frame = gdb.selected_frame()
            print("LOOK HERE FINISH", frame.name())
            addr = frame.read_var("slen")
            daemon = frame.read_var("dnsmasq_daemon").dereference()
            netlinkfd = daemon["netlinkfd"]
            print(f"Address: {addr}")
            print(f"Netlink: {netlinkfd}")
            return True

        def stopBreak():
            frame = gdb.selected_frame()
            print("LOOK HERE BREAK", frame.name())
            addr = frame.read_var("addr")
            print(f"Address at beggining of function: {addr}")
            if stopped := self.myFinishPoint(frame, definition=stopFinish):
                print("Stop point set successfully")
            else:
                print("Failed")
            return False

        print(
            f"Setting breakpoint {self.myBreakPoint('netlink_init', definition=stopBreak)}"
        )

    def cache_init(self):
        def stopFinish():
            frame = gdb.selected_frame()
            crec = frame.read_var("crecp")
            i = frame.read_var("i")
            cachesize = frame.read_var("daemon->cachesize")
            print(f"crecp after cache_init: {crec}")
            print(f"Amount of crec: {i}")
            print(f"New Cachesize: {cachesize}")
            return True

        def stopBreak():
            frame = gdb.selected_frame()
            crec = frame.read_var("crecp")
            i = frame.read_var("i")
            cachesize = frame.read_var("daemon->cachesize")
            print(f"crecp after cache_init: {crec}")
            print(f"Amount of crec: {i}")
            print(f"New Cachesize: {cachesize}")
            if stopped := self.myFinishPoint(frame, definition=stopFinish):
                print(f"Stop point: {stopped}")
            else:
                print("Failed cache_init")
            return False

        print(
            f"Setting breakpoint: {self.myBreakPoint('cache_init', definition=stopBreak)}"
        )


myBreakpoint = MyBreakpoint()
