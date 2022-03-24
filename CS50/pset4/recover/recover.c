#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCKSIZE 512
typedef uint8_t BYTE;

bool header(uint8_t buffer[]);

int main(int argc, char *argv[])
{
    // command line arguement checker
    if (argc != 2)
    {
        printf("Usage: ./recover file\n");
        return 1;
    }

    char *inputfile = argv[1];

    // error opening file checker
    if (inputfile == NULL)
    {
        printf("Usage: ./recover file\n");
        return 1;
    }
    // open file
    FILE *inptr = fopen(inputfile, "r");
    if (inptr == NULL)
    {
        printf("Unable to open\n");
        return 1;
    }

    // 001
    char filename[8];
    // output file
    FILE *outptr = NULL;
    //buffer
    uint8_t buffer[BLOCKSIZE];
    // jpg counter
    int jpgcounter = 0;

    while (fread(buffer, sizeof(uint8_t), BLOCKSIZE, inptr) || feof(inptr) == 0)
    {
        // start of new jpeg file
        if (header(buffer))
        {
            if (outptr != NULL)
            {
                fclose(outptr);
            }
            sprintf(filename, "%03i.jpg", jpgcounter);
            // open new file
            outptr = fopen(filename, "w");
            jpgcounter++;
        }

        // write into new file
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, outptr);
        }
    }

    // close files
    if (outptr == NULL)
    {
        fclose(outptr);
    }
    if (inptr == NULL)
    {
        fclose(inptr);
    }

    return 0;
}

bool header(uint8_t buffer[])
{
    return (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0);
}