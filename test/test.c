#define NULL ((void *)0)
static void **hash = NULL;

static void **hash_bucket(char *name)
{
  unsigned int c, val = 017465; /* Barker code - minimum self-correlation in cyclic shift */
  const unsigned char *mix_tab = (const unsigned char*)typestr; 
  while((c = (unsigned char) *name++))
    {
      /* don't use tolower and friends here - they may be messed up by LOCALE */
      if (c >= 'A' && c <= 'Z')
        c += 'a' - 'A';
      val = ((val << 7) | (val >> (32 - 7))) + (mix_tab[(val + c) & 0x3F] ^ c);
    } 
  /* hash_size is a power of two */
  return hash_table + ((val ^ (val >> 16)) & (hash_size - 1));
}

int main(int argc, char **argv){
  char *name = "Nicholas";
  hash = hash_bucket(name);
  printf(%p, hash);
  return 0;
}
