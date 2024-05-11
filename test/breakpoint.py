import gdb

## Clean up

for bp in gdb.breakpoints():
    bp.delete()


class MyBreakpoint:
    def __init__(self):
        self.rand_init()
        self.main()

    def rand_init(self):
        class RandInit(gdb.Breakpoint):
            def stop(self):
                frame = gdb.selected_frame()
                old = frame.older()
                i = old.read_var("i")
                var = frame.read_var("var")
                print("Index:", i, "Function Val:", var)
                return True

        test = RandInit("testFunc")
        print(type(test))

    def main(self):
        class LoopBreak(gdb.Breakpoint):
            def stop(self):
                print("Reached Main")
                return False

        loop = LoopBreak("main")


myBreakpoint = MyBreakpoint()
