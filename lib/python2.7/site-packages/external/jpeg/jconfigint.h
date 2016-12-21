#define BUILD "20161115"
#ifdef _MSC_VER  /* Windows */
#define INLINE __inline
#else
#define INLINE inline __attribute__((always_inline))
#endif
#define PACKAGE_NAME "libjpeg-turbo"
#define VERSION "1.5.1"
#if (__WORDSIZE==64 && !defined(__native_client__)) || defined(_WIN64)
#define SIZEOF_SIZE_T 8
#else
#define SIZEOF_SIZE_T 4
#endif
