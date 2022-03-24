#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get height from user
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);



    // v = row , s = " " , x = column
    // construct
    for (int v = 0; v < h; v++)
    {
        //number of " " per line

        for (int s = 0; s < h - v - 1 ; s++)
        {
            printf(" ");
        }

        // number of "#" per line
        for (int x = 0; x <= v; x++)
        {
            printf("#");
        }

        // next line
        printf("\n");
    }
}