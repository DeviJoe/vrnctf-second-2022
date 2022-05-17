#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>
#include "Log.h"
#include "MetaString.h"


int main(int argc, char *argv[])
{
  const char *flag = OBFUSCATED("vrnctf{f0rks_4re_am4zing_wh3n_th3r3_is_tr33_of_th3m}");

  for (int i = 0; i < strlen(flag); i++)
  {
    char f[] = {0, 0};

    f[0] = flag[i];

    pid_t pid = fork();

    if (pid == 0)
    {
      memset(argv[0], 0, strlen(argv[0]));

      argv[0][0] = flag[i];

    } else if (pid < 0)
    {
      perror("fork()");
    } else
    {
      break;
    }
  }

  while(wait(NULL) > 0);

  return 0;
}