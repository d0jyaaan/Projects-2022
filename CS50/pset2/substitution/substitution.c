#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int checker = 0;
string UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
string LOWER = "abcdefghijklmnopqrstuvwxyz";

int main(int argc, string argv[])
{
    // key conditions
    if (argc == 2)
    {
        // length checker
        int n = strlen(argv[1]);
        if (n == 26)
        {
            // for every char
            for (int i = 0; i < n; i++)
            {
                // check is alphabet or not
                if (isalpha(argv[1][i]))
                {
                    // repetition checker
                    for (int j = 0; j < n - 1; j++)
                    {
                        for (int k = j + 1; k < n; k++)
                        {
                            // repetition checker lower and upper case
                            if (argv[1][j] == argv[1][k])
                            {
                                printf("Conditions: No repetitions.\n");
                                return 1;
                            }
                            else
                            {
                                checker ++;
                            }
                        }
                    }
                }
                else
                {
                    printf("Usage: ./substitution key\n");
                    return 1;
                }
            }
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    else
    {
        printf("\n");
        return 1;
    }

    // if the key satisfies,
    if (checker == 8450)
    {
        // get plaintext
        string plaintext = get_string("plaintext: ");
        int length = strlen(plaintext);
        printf("ciphertext: ");
        for (int l = 0; l < length; l++)
        {
            // ciphertext
            if ((plaintext[l] >= 'A' && plaintext[l] <= 'Z') || (plaintext[l] >= 'a' && plaintext[l] <= 'z'))
            {
                // alphabet matcher
                for (int m = 0; m < 26; m++)
                {
                    // lowercase converter and checker
                    if (islower(plaintext[l]))
                    {
                        if (plaintext[l] == LOWER[m])
                        {
                            printf("%c", tolower(argv[1][m]));
                        }
                    }
                    // uppercase converter and checker
                    else if (isupper(plaintext[l]))
                    {
                        if (plaintext[l] == UPPER[m])
                        {
                            printf("%c", toupper(argv[1][m]));
                        }
                    }
                }
            }
            else
            {
                printf("%c", plaintext[l]);
            }
        }
        printf("\n");
    }
    return 0;
}
