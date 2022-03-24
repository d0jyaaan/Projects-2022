#include <stdio.h>
#include <math.h>
#include <cs50.h>

float cash[4] = {1, 5, 10, 25};
int change = 0;

int main(void)
{
    // get input
    float input;
    do
    {
        input = get_float("Change owed: ");
    }
    while (input < 0);

    // round
    int in = round(input * 100);

    // change counter
    while (in > 0)
    {
        // 0.25
        if (in >= cash[3])
        {
            in -= cash[3];
            change++;
            continue;
        }
        // 0.1
        if (in >= cash[2])
        {
            in -= cash[2];
            change++;
            continue;
        }
        // 0.05
        if (in >= cash[1])
        {
            in -= cash[1];
            change++;
            continue;
        }
        // 0.1
        if (in >= cash[0])
        {
            in -= cash[0];
            change++;
            continue;
        }
    }
    // print change
    printf("%i\n", change);
}