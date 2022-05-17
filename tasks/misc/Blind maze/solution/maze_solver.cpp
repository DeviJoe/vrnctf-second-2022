#include <iostream>

int main()
{
  int8_t cipher_text[40] = {0};
  uint64_t key = 0xf965a75d5779cb5d;
  int idx = 0;

  cipher_text[idx++] = 0x2b;
  cipher_text[idx++] = 0xb9;
  cipher_text[idx++] = 0x17;
  cipher_text[idx++] = 0x34;
  cipher_text[idx++] = 0x29;
  cipher_text[idx++] = 0xc1;
  cipher_text[idx++] = 0x1e;
  cipher_text[idx++] = 0x9d;
  cipher_text[idx++] = 0x6d;
  cipher_text[idx++] = 0xf8;
  cipher_text[idx++] = 10;
  cipher_text[idx++] = 8;
  cipher_text[idx++] = 0x3f;
  cipher_text[idx++] = 0xcb;
  cipher_text[idx++] = 0x54;
  cipher_text[idx++] = 0x97;
  cipher_text[idx++] = 0x39;
  cipher_text[idx++] = 0x94;
  cipher_text[idx++] = 0x14;
  cipher_text[idx++] = 99;
  cipher_text[idx++] = 0x27;
  cipher_text[idx++] = 0x94;
  cipher_text[idx++] = 0x3a;
  cipher_text[idx++] = 0x8e;
  cipher_text[idx++] = 0x69;
  cipher_text[idx++] = 0xb8;
  cipher_text[idx++] = 0x26;
  cipher_text[idx++] = 0x24;
  cipher_text[idx++] = 0x6d;
  cipher_text[idx++] = 0xf8;
  cipher_text[idx++] = 0xd;
  cipher_text[idx++] = 0xcd;
  cipher_text[idx++] = 0x2f;
  cipher_text[idx++] = 0xaf;
  cipher_text[idx++] = 4;
  cipher_text[idx++] = 0x5d;
  cipher_text[idx++] = 0x5d;

  for (idx = 0; idx < 37; idx++)
  {
    cipher_text[idx] = cipher_text[idx] ^ (uint8_t)(key >> (int8_t)(((uint)idx & 7) << 3));
  }

  std::cout << cipher_text;
}