#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>


char *ct = "vyf5bBCsbxU^1oC0yI1hTtxe{wi9~%gsr5&q}10mg24ebo'ebr{3iU~b5nyu^;s}";

char *code = "deny";

void xor(char buf[], char *code, char *msg, int len, bool reverse)
{
  char tmp[100];
  memset(tmp, 0, 100);

  for (int i = 0; i < len; i++)
  {
    if (reverse)
    {
      tmp[i] = code[i % strlen(code)] ^ msg[i];
    }
    else
    {
      tmp[i] = code[strlen(code) - i % strlen(code) - 1] ^ msg[i];
    }
  }

  memcpy(buf, tmp, 100);
}


void demingle(char *msg, char buf1[], char buf2[], int len)
{
  memset(buf1, 0, 100);
  memset(buf2, 0, 100);

  for (size_t i = 0; i < len / 2; i++)
  {
    buf1[i] = msg[i * 2];
    buf2[i] = msg[i * 2 + 1];
  }
}


int main(int argc, char *argv[])
{
  char buf[100];
  int c = 1;
  int len = strlen(ct);
  char buf1[100];
  char buf2[100];

  memcpy(buf, ct, 64);

  for (size_t i = 0;;i++)
  {
    memset(buf1, 0, 100);
    memset(buf2, 0, 100);

    demingle(buf, buf1, buf2, len);

    len /= 2;

    if (fork())
    {
      xor(buf1, code, buf1, len, false);
      memset(buf, 0, 100);
      memcpy(buf, buf1, 100);
    }
    else
    {
      xor(buf2, code, buf2, len, true);
      memset(buf, 0, 100);
      memcpy(buf, buf2, 100);
    }
  }

  return 0;
}