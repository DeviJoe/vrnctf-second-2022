#include <iostream>
#include <cstring>
#include <cassert>
#include "obfuscate.h"


static const char logo[] =
"    ____  ___           __   __  ___               \n"
"   / __ )/ (_)___  ____/ /  /  |/  /___ _____  ___ \n"
"  / __  / / / __ \\/ __  /  / /|_/ / __ `/_  / / _ \\\n"
" / /_/ / / / / / / /_/ /  / /  / / /_/ / / /_/  __/\n"
"/_____/_/_/_/ /_/\\__,_/  /_/  /_/\\__,_/ /___/\\___/ \n";

static const int width = 24 * 3;
static const int height = 24 * 3;

static const char verbose_arg[] = "-vvvv";

static const uint8_t maze[] =
{
  0, 0, 0, 0, 0, 0, 0,
  0, 0, 242, 231, 207, 243, 252, 201,
  243, 231, 127, 130, 36, 72, 146, 36,
  73, 146, 4, 64, 130, 36, 72, 146,
  36, 73, 146, 4, 64, 242, 60, 121,
  158, 36, 121, 158, 252, 127, 18, 0,
  1, 128, 32, 1, 130, 0, 64, 18,
  0, 1, 128, 32, 1, 130, 0, 64,
  158, 252, 255, 159, 63, 127, 158, 255,
  79, 128, 36, 64, 0, 0, 64, 0,
  0, 73, 128, 36, 64, 0, 0, 64,
  0, 0, 73, 254, 36, 79, 254, 63,
  207, 159, 63, 73, 130, 36, 9, 2,
  32, 9, 144, 32, 8, 130, 36, 9,
  2, 32, 9, 144, 32, 8, 158, 228,
  201, 243, 231, 249, 243, 228, 121, 144,
  4, 72, 0, 4, 0, 2, 4, 65,
  144, 4, 72, 0, 4, 0, 2, 4,
  65, 146, 39, 207, 243, 255, 127, 254,
  60, 79, 18, 32, 9, 18, 0, 0,
  16, 36, 72, 18, 32, 9, 18, 0,
  0, 16, 36, 72, 158, 63, 201, 243,
  63, 255, 243, 231, 79, 130, 32, 73,
  16, 32, 1, 2, 0, 64, 130, 32,
  73, 16, 32, 1, 2, 0, 64, 242,
  60, 73, 158, 63, 127, 158, 255, 127,
  130, 4, 65, 130, 0, 1, 18, 36,
  0, 130, 4, 65, 130, 0, 1, 18,
  36, 0, 254, 60, 79, 158, 63, 249,
  243, 228, 127, 0, 32, 72, 16, 32,
  9, 128, 4, 64, 0, 32, 72, 16,
  32, 9, 128, 4, 64, 254, 63, 121,
  158, 231, 201, 159, 60, 127, 2, 0,
  1, 128, 4, 8, 146, 0, 65, 2,
  0, 1, 128, 4, 8, 146, 0, 65,
  254, 60, 255, 255, 252, 201, 147, 63,
  79, 128, 36, 1, 0, 0, 73, 0,
  32, 72, 128, 36, 1, 0, 0, 73,
  0, 32, 72, 242, 228, 249, 255, 63,
  201, 255, 60, 79, 18, 4, 8, 2,
  32, 73, 16, 4, 65, 18, 4, 8,
  2, 32, 73, 16, 4, 65, 242, 231,
  127, 242, 39, 79, 146, 231, 121, 2,
  0, 1, 18, 4, 64, 146, 32, 8,
  2, 0, 1, 18, 4, 64, 146, 32,
  8, 254, 63, 121, 254, 252, 79, 146,
  231, 121, 130, 32, 72, 128, 32, 72,
  18, 4, 65, 130, 32, 72, 128, 32,
  72, 18, 4, 65, 242, 60, 79, 158,
  231, 73, 242, 252, 73, 18, 4, 65,
  18, 4, 65, 130, 0, 72, 18, 4,
  65, 18, 4, 65, 130, 0, 72, 146,
  63, 201, 243, 60, 207, 147, 252, 127,
  18, 32, 9, 128, 0, 8, 146, 4,
  0, 18, 32, 9, 128, 0, 8, 146,
  4, 0, 242, 231, 249, 159, 255, 79,
  158, 231, 121, 2, 4, 8, 18, 0,
  72, 16, 0, 73, 2, 4, 8, 18,
  0, 72, 16, 0, 73, 146, 231, 201,
  243, 231, 201, 147, 63, 79, 146, 32,
  65, 16, 32, 73, 146, 32, 72, 146,
  32, 65, 16, 32, 73, 146, 32, 72,
  146, 60, 121, 158, 63, 127, 242, 228,
  73, 146, 4, 9, 128, 0, 0, 0,
  4, 65, 146, 4, 9, 128, 0, 0,
  0, 4, 65, 158, 231, 249, 255, 252,
  249, 255, 63, 121, 2, 32, 1, 2,
  0, 9, 0, 32, 9, 2, 32, 1,
  2, 0, 9, 0, 32, 9, 242, 63,
  121, 254, 231, 121, 254, 231, 121, 18,
  0, 72, 2, 36, 65, 144, 4, 64,
  18, 0, 72, 2, 36, 65, 144, 4,
  64, 242, 252, 79, 242, 60, 207, 147,
  252, 79, 130, 4, 64, 144, 0, 1,
  130, 0, 72, 130, 4, 64, 144, 0,
  1, 130, 0, 72, 242, 228, 79, 158,
  60, 121, 254, 228, 121, 18, 4, 73,
  130, 36, 72, 0, 36, 65, 18, 4,
  73, 130, 36, 72, 0, 36, 65, 242,
  255, 201, 159, 231, 207, 255, 63, 127,
  0, 0, 0, 0, 0, 0, 0, 0
};


typedef struct pos_s
{
  int x, y;
} pos_t;


bool get_pos(int x, int y)
{
  return maze[(y * width + x) / 8] & 0x01 << (y * width + x) % 8;
}


bool check_pos(int x, int y)
{
  if (y < height && x < width && get_pos(x, y))
  {
    return true;
  }

  return false;
}


bool check_verbose_flag(char *first_arg)
{
  bool ret = false;

  switch (strlen(first_arg))
  {
  case 2:
    if (strncmp(first_arg, verbose_arg, 2) == 0)
    {
      std::cout << "There are no Easter Eggs in this program." << std::endl;
    }
    break;

  case 3:
    if (strncmp(first_arg, verbose_arg, 3) == 0)
    {
      std::cout << "There really are no Easter Eggs in this program." << std::endl;
    }
    break;

  case 4:
    if (strncmp(first_arg, verbose_arg, 4) == 0)
    {
      std::cout << "Didn't I already tell you that there are no Easter Eggs in this program?" << std::endl;
    }
    break;

  case 5:
    if (strncmp(first_arg, verbose_arg, 5) == 0)
    {
      std::cout << "All right, you win. I'll turn the light on. But you still need to go throught this maze..." << std::endl;
      ret = true;
    }
  default:
    break;
  }

  return ret;
}


inline void update_pos(char input, pos_t *pos, bool verbose = false)
{
  switch (tolower(input)) {
      case 'w':
        if (check_pos(pos->x, pos->y - 1))
        {
          pos->y--;
          if (verbose)
          {
            std::cout << "Going up;" << std::endl;
          }
        } else if (verbose)
        {
          std::cout << "OOPS! Dead-end;" << std::endl;
        }
        else
        {
        }
        break;

      case 's':
        if (check_pos(pos->x, pos->y + 1))
        {
          pos->y++;
          if (verbose)
          {
            std::cout << "Going down;" << std::endl;
          }
        } else if (verbose)
        {
          std::cout << "OOPS! Dead-end;" << std::endl;
        }
        else
        {
        }
        break;

      case 'd':
        if (check_pos(pos->x + 1, pos->y))
        {
          pos->x++;
          if (verbose)
          {
            std::cout << "Going right;" << std::endl;
          }
        } else if (verbose)
        {
          std::cout << "OOPS! Dead-end;" << std::endl;
        }
        else
        {
        }
        break;

      case 'a':
        if (check_pos(pos->x - 1, pos->y))
        {
          pos->x--;
          if (verbose)
          {
            std::cout << "Going left;" << std::endl;
          }
        } else if (verbose)
        {
          std::cout << "OOPS! Dead-end;" << std::endl;
        }
        else
        {

        }
        break;

      case '\r':
      case '\n':
        break;

      default:
        if (verbose)
        {
          std::cout << "Incorrect symbol;" << std::endl;
        }
        break;
    }
}


inline int get_input_argv_size(int argc, char *argv[], bool verbose, uint32_t &argv_pos)
{
  int result = 0;

  if (argc >= 3)
  {
    result = strlen(argv[2]);
    argv_pos = 2;
  }
  else if (argc >= 2 && !verbose)
  {
    result = strlen(argv[1]);
    argv_pos = 1;
  }

  return result;
}


int main(int argc, char *argv[]) {
  int input;
  bool verbose = false;
  pos_t pos  = {1, 1};
  int ctr = 0;
  uint32_t argv_pos = 0;

  std::cout << logo << "This program accepts args." << std::endl << std::endl;

  if (argc >= 2)
  {
    verbose = check_verbose_flag(argv[1]);
  }

  const int argv_len = get_input_argv_size(argc, argv, verbose, argv_pos);

  while (pos.x < width - 2 || pos.y < height - 2 )
  {
    if (ctr < argv_len)
    {
      input = argv[argv_pos][ctr];
      ctr++;
    }
    else
    {
      input = getc(stdin);
    }

    update_pos(input, &pos, verbose);
  }

  std::cout << std::endl << "Congratulations! You've won." << std::endl;
  std::cout << AY_OBFUSCATE("vrnctf{d03s_bl1nd_m4z3_w4s_s0_h4rd}\n");

  return 0;
}