#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>

char *flag = "vrnctf{4t_wh1ch_l00p_h4d_y0u_f1nd_4nsw3r_t0_d3n14bl3_3ncrypt1on}";

char *code = "deny";

char *flags[] = {
  "vrnc",
  "tf{4",
  "t_wh",
  "1ch_",
  "l00p",
  "_h4d",
  "_y0u",
  "_f1n",
  "d_4n",
  "sw3r",
  "_t0_",
  "d3n1",
  "4bl3",
  "_3nc",
  "rypt",
  "1on}"
};

/*
vrnc tf{4 t_wh 1ch_ l00p _h4d _y0u _f1n d_4n sw3r _t0_ d3n1 4bl3 _3nc rypt 1on}

*/

void mingle(char buf[], char *msg1, char *msg2)
{
  memset(buf, 0, 100);

  for (int i = 0; i < strlen(msg1); i++)
  {
    buf[i * 2] = msg1[i];
    buf[i * 2 + 1] = msg2[i];
  }
}


void xor(char buf[], char *code, char *msg, bool reverse)
{
  memset(buf, 0, 100);

  for (int i = 0; i < strlen(msg); i++)
  {
    if (reverse)
    {
      buf[i] = code[i % strlen(code)] ^ (!msg[i]);
    }
    else
    {
      buf[i] = code[i % strlen(code)] ^ msg[i];
    }
  }
}


int main(int argc, char *argv[])
{
  char **map = flags;
  char codes[16][100];
  int c = 16;
  for (size_t i = 0; i < 4; i++)
  {
    c /= 2;

    for (size_t j = 0; i < c; i++)
    {
      char buf1[100];
      char buf2[100];

      xor(buf1, code, map[j * 2], false);
      xor(buf2, code, map[j * 2 + 1], true);

      mingle(codes[j], buf1, buf2);
    }

    map = codes;
  }

  printf("%s \n", map[0]);

  return 0;
}