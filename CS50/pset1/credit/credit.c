#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long credit_card;
    long credit_check;
    int total = 0;
    int position = 0;
    int digit_count = 0;


    do
    {
        credit_card = get_long("Number: ");

        credit_check = credit_card;

        while (credit_card != 0)
        {
            // every other position starting from second digit
            if (position % 2 != 0)
            {
                // x = temporary number after *2
                int x = (credit_card % 10) * 2;

                // if x is 2 digits, seperate it
                if (x > 9)
                {
                    // total + 14 % 10 + 4 from (14 / 10)
                    total += x % 10 + (x / 10) % 10;
                }
                else
                {
                    // add x to total
                    total += x;
                }
            }

            // every other position starting from first digit
            else
            {
                // add every other position starting from first digit to total
                total += (credit_card % 10);
            }

            // next number
            credit_card = credit_card / 10;
            position++; // + 1 position
            digit_count++; // + 1 to digit counter

        }
    }

    while (credit_card != 0);

    // credit checker
    if (total % 10 == 0)
    {
        // card type checker
        // AMEX checker
        int AMEX = credit_check / 10000000000000;
        if ((AMEX == 34 || AMEX == 37) && digit_count == 15)
        {
            printf("AMEX\n");
            return 0;
        }

        if (digit_count == 13 || digit_count == 16)
        {
            // MASTERCARD checker
            int MASTERCARD = credit_check / 100000000000000;
            if ((MASTERCARD >= 51 && MASTERCARD <= 55) && digit_count == 16)
            {
                printf("MASTERCARD\n");
                return 0;
            }

            // VISA checker
            int VISA_1 = credit_check / 1000000000000000; // visa 16 digit
            int VISA_2 = credit_check / 1000000000000; // visa 13 digit

            if ((VISA_1 == 4 && digit_count == 16) || (VISA_2 == 4 && digit_count == 13))
            {
                printf("VISA\n");
                return 0;
            }

        }
        // if dont fit any condition, print invalid
        printf("INVALID\n");
    }

    // invalid if not 0
    else
    {
        printf("INVALID\n");
    }
}