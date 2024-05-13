import gdb


class MyBreakpoint:
    def __init__(self):
        self.clean()
        self.main()
        # self.rand_init()
        # self.read_opts()
        # self.netlink_init()
        # self.cache_init()
        self.check_dns_listeners()

    def myWatchPoint(self, expr, factory=None):
        class WatchPoint(gdb.Breakpoint):
            def __init__(self, expr, factory):
                if not isinstance(self, gdb.Breakpoint):
                    print("Something weird")
                super().__init__(expr, gdb.BP_WATCHPOINT)
                self.expr = expr
                if factory:
                    self.stop = factory(self.delete)
                else:
                    self.stop = self.definition

            def definition(self):
                return True

        return WatchPoint(expr, factory)

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
                self.name = frame.name()
                if definition:
                    self.stop = definition
                else:
                    self.stop = self.definition

            def definition(self):
                print(f"Completed function {self.name}")
                return True

            def out_of_scope(self):
                print(f"Abnormal Finish {self.name}")

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
            # if stopped := self.myFinishPoint(frame, definition=stopFinish):
            #    print("Stop point set successfully")
            # else:
            #    print("Failed")
            return False

        print(
            f"Setting breakpoint {self.myBreakPoint('netlink_init', definition=stopBreak)}"
        )

    def cache_init(self):
        def stopFinish():
            return True

        def stopWatch():
            frame = gdb.selected_frame()
            if frame.name() == "cache_init":
                i = frame.read_var("i")
                crec = frame.read_var("crecp")
                print(f"({frame.name()}) {i}: {crec.dereference()}")
            return False

        def stopBreak():
            frame = gdb.selected_frame()
            crec = frame.read_var("crecp")
            i = frame.read_var("i")
            daemon = frame.read_var("dnsmasq_daemon").dereference()
            cachesize = daemon["cachesize"]
            print(f"crecp after cache_init: {crec}")
            print(f"Amount of crec: {i}")
            print(f"New Cachesize: {cachesize}")
            self.myFinishPoint(frame, definition=stopFinish)
            iWatch = self.myWatchPoint("i", stopWatch)
            if iWatch:
                print(f"iWatch created: {iWatch}")
            return False

        print(
            f"Setting breakpoint: {self.myBreakPoint('cache_init', definition=stopBreak)}"
        )

    def check_dns_listeners(self):
        def stop_watch_server_factory(delete):
            def stop_watch_server():
                frame = gdb.selected_frame()
                if frame.read_var("serverfdp"):
                    server = frame.read_var("serverfdp").dereference()
                    print(
                        f"Server fd: {server['fd']} -> {server['interface'].string()}"
                    )
                else:
                    delete()
                return True

            return stop_watch_server

        def stop_watch_listener_factory(delete):
            def stop_watch_listener():
                frame = gdb.selected_frame()
                if frame.read_var("listener"):
                    listener = frame.read_var("listener").dereference()
                    print(
                        f"Listener fd: {listener['fd']}, \
                        tcpfd: {listener['tcpfd']}, \
                        tftpfd: {listener['tftpfd']}, \
                        used: {listener['used']}"
                    )
                    if listener["iface"]:
                        iface = listener["iface"].dereference()
                        print(f"iface: {iface}")
                else:
                    delete()
                return False

            return stop_watch_listener

        def stop_watch_rfl_factory(delete):
            def stop_watch_rfl():
                frame = gdb.selected_frame()
                if frame.read_var("rfl"):
                    rfl = frame.read_var("rfl").dereference()
                    rfd = rfl["rfd"].dereference()
                    next = rfl["next"]

                # while next:
                #    rfl = next.dereference()
                #    rfd = rfl["rfd"].dereference()
                #    next = rfl["next"]
                #    print(f"rfd: {rfd}")
                else:
                    delete()
                return False

            return stop_watch_rfl

        def check_dns_listeners_stop_break():
            frame = gdb.selected_frame()
            print("Break set at set_dns_listeners")
            server_watch = self.myWatchPoint(
                "serverfdp", factory=stop_watch_server_factory
            )
            listener_watch = self.myWatchPoint(
                "listener", factory=stop_watch_listener_factory
            )
            rfl_watch = self.myWatchPoint("rfl", factory=stop_watch_rfl_factory)

            def check_dns_listeners_stop_finish():
                server_watch.delete()
                listener_watch.delete()
                rfl_watch.delete()
                return True

            self.myFinishPoint(frame, definition=check_dns_listeners_stop_finish)
            return False

        check_dns_listener_watch = self.myBreakPoint(
            "check_dns_listeners", definition=check_dns_listeners_stop_break
        )

    def enumerate_interfaces(self):
        pass


myBreakpoint = MyBreakpoint()
