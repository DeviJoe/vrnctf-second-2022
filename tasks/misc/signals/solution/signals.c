#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include "Log.h"
#include "MetaString.h"


char alphabet[] = "abcdefghijklmnopqrstuvwxyz_{}";

int get_index(char c) {
  char *e = strchr(alphabet, c);

  if (e == NULL) {
    return -1;
  }

  return (int)(e - alphabet);
}

int main() {
  const char *flag = OBFUSCATED("vrnctf{try_to_catch_me_before_you_d_e}");

  int pid;
  int sig;

  printf("Whom I need to \033[0;31mkill\033[0m?\n");
  scanf("%d", &pid);

  for (int i = 0; i < strlen(flag); i++)
  {
    sig = get_index(flag[i]) + 1;

    kill(pid, sig);

    sleep(1);
  }

  kill(pid, SIGKILL);

  return 0;
}