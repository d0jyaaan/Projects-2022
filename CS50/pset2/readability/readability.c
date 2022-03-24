#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int sentence = 0;
int letter = 0;
int word = 0;

int main(void)
{
    // prompt user for sentence
    string text = get_string("Text: ");

    // number of letters
    // total number of letters before checking
    int length = strlen(text);

    // counnter
    for (int i = 0; i < length; i++)
    {
        // letters counter
        if ((text[i] >= 'A' && text[i] <= 'Z') || (text[i] >= 'a' && text[i] <= 'z'))
        {
            letter++;
        }
        // words counter
        else if (text[i] == ' ')
        {
            word++;
        }
        // sentences counter
        else if ((text[i] == '!') || (text[i] == '?') || (text[i] == '.'))
        {
            sentence++;
        }
    }
    word++;

    // index calculator
    // L (average number of letters per 100 words)
    float L = (float)letter / ((float)word / 100);

    // S (average number of sentences per 100 words)
    float S = (float)sentence / ((float)word / 100);

    // index equation
    float index = 0.0588 * L - 0.296 * S - 15.8;

    // round
    int final_index = round(index);

    // print grade 'x'
    // less than 1
    if (final_index < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    // more than 16
    else if (final_index > 16)
    {
        printf("Grade 16+\n");
    }
    // between 1 and 16
    else
    {
        printf("Grade %i\n", final_index);
    }
}