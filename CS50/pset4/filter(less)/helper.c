#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // height
    for (int i = 0; i < height; i++)
    {
        // width
        for (int j = 0; j < width; j++)
        {
            // calculation
            float average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.00;
            // round off
            int avrg = round((float)(average));

            // assign new pixel RGB
            image[i][j].rgbtRed = avrg;
            image[i][j].rgbtBlue = avrg;
            image[i][j].rgbtGreen = avrg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // height
    for (int i = 0; i < height; i++)
    {
        // width
        for (int j = 0; j < width; j++)
        {
            // sepia red cal
            float sepiaRed = (.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            // sepia green cal
            float sepiaGreen = (.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            // sepia blue cal
            float sepiaBlue = (.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            // round off values more than 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            // assign values
            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtBlue = round(sepiaBlue);
            image[i][j].rgbtGreen = round(sepiaGreen);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            // assign tmp with opposite side value (right)
            int red = image[i][width - j - 1].rgbtRed;
            int green = image[i][width - j - 1].rgbtGreen;
            int blue = image[i][width - j - 1].rgbtBlue;

            // assign values from right with values starting on left
            image[i][width - j - 1].rgbtRed = image[i][j].rgbtRed;
            image[i][width - j - 1].rgbtGreen = image[i][j].rgbtGreen;
            image[i][width - j - 1].rgbtBlue = image[i][j].rgbtBlue;

            // assign values from left with values starting from right
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int red[height][width];
    int green[height][width];
    int blue[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0;
            int sumBlue = 0;
            int sumGreen = 0;
            float divide = 0.00;

            // position around [i][j]
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if ((i + k < 0) || (i + k > height - 1) || (j + l < 0) || (j + l > width - 1))
                    {
                        continue;
                    }
                    // sum of rgb
                    sumRed += image[i + k][j + l].rgbtRed;
                    sumGreen += image[i + k][j + l].rgbtGreen;
                    sumBlue += image[i + k][j + l].rgbtBlue;
                    // number to divide by
                    divide++;
                }
            }

            // blur value cal
            red[i][j] = round(sumRed / divide);
            green[i][j] = round(sumGreen / divide);
            blue[i][j] = round(sumBlue / divide);
        }
    }
    // assign new values
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = red[i][j];
            image[i][j].rgbtGreen = green[i][j];
            image[i][j].rgbtBlue = blue[i][j];
        }
    }
    return;
}

