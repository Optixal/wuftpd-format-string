#include <stdarg.h>
#include <stdio.h>

void vout(char *fmt, ...);
/*char fmt1 [] = "%s  %s  %s\n";*/

int main(void)
{
    char fmt1 [] = "%x %x %x %x %2$x\n";
    vout(fmt1);
}

void vout(char *fmt, ...)
{
    va_list arg_ptr;
    char buf[100];

    va_start(arg_ptr, fmt);
    vsnprintf(buf, sizeof(buf), fmt, arg_ptr);
    va_end(arg_ptr);

    printf("The buffer is: %s\n", buf);
}
