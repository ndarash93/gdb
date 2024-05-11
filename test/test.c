__attribute__((noinline)) int testFunc(int var) { return var + var; }

int main(int argc, char **argv) {
  // char *help = "Hello World!";
  int i = 0;
  while (i < 10) {
    int one = testFunc(5);
    i++;
  }
  // strcpy(test1.name, "Hello from test1");
  return 0;
}
