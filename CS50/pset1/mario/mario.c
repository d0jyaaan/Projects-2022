#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int h;
    // get h
    do
    {
        h = get_int("height: ");
    }
    while (h < 1 || h > 8);

    for (int i = 0; i < h; i++)
    {
        // print left side
        for (int k = 0; k < h - i - 1; k++)
        {
            printf(" ");
        }

        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        // space
        printf("  ");

        // print right side
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}