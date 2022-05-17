#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>


char alphabet[] = "abcdefghijklmnopqrstuvwxyz_{}";
/*                12345678901234567890123456 */

char get_char(int c) {
  return alphabet[c - 1];
}

void handler(int sig)
{
  printf("%c \n", get_char(sig));
}

int main() {
  struct sigaction act;
  sigset_t   set;
  int i;

  memset(&act, 0, sizeof(act));
  act.sa_handler = handler;

  sigfillset(&act.sa_mask);
  act.sa_flags = SA_RESTART;

  for (i = 1; i <= strlen(alphabet); i++)
  {
    sigaction(i, &act, NULL);
  }

  for(;;) {}

  return 0;
}