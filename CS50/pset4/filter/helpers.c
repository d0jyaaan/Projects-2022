#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // cal the average
            float average = ((float)image[i][j].rgbtRed + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtBlue) / 3.00;

            // round off average
            int avg = round(average);
            // assign new values
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
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
            // assign values starting from right side
            int red = image[i][width - j - 1].rgbtRed;
            int green = image[i][width - j - 1].rgbtGreen;
            int blue = image[i][width - j - 1].rgbtBlue;

            // assign values on right side with left side
            image[i][width - j - 1].rgbtRed = image[i][j].rgbtRed;
            image[i][width - j - 1].rgbtGreen = image[i][j].rgbtGreen;
            image[i][width - j - 1].rgbtBlue = image[i][j].rgbtBlue;

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
    int a[height][width];
    int b[height][width];
    int c[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumred = 0;
            int sumgreen = 0;
            int sumblue = 0;
            float divide = 0.00;

            // 3 x 3 grid
            for (int k = -1; k < 2 ; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // out of bounds checker
                    if ((i + k < 0) || (i + k > height - 1) || (j + l < 0) || (j + l > width - 1))
                    {
                        continue;
                    }
                    // sum
                    sumred += image[i + k][j + l].rgbtRed;
                    sumgreen += image[i + k][j + l].rgbtGreen;
                    sumblue += image[i + k][j + l].rgbtBlue;

                    divide++;
                }
            }

            // temp array
            a[i][j] = round(sumred / divide);
            b[i][j] = round(sumgreen / divide);
            c[i][j] = round(sumblue / divide);
        }
    }

    // assign new values
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = a[i][j];
            image[i][j].rgbtGreen = b[i][j];
            image[i][j].rgbtBlue = c[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int a[height][width];
    int b[height][width];
    int c[height][width];

    int gx[3][3] =
    {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int gy[3][3] =
    {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}

    };

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float gx_sumred = 0;
            float gx_sumgreen = 0;
            float gx_sumblue = 0;

            float gy_sumred = 0;
            float gy_sumgreen = 0;
            float gy_sumblue = 0;

            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if ((i + k < 0) || (i + k > height - 1) || (j + l < 0) || (j + l > width - 1))
                    {
                        continue;
                    }
                    int x = 1 + k;
                    int y = 1 + l;
                    // Gx sum
                    gx_sumred += ((image[i + k][j + l].rgbtRed) * gx[x][y]);
                    gx_sumgreen += ((image[i + k][j + l].rgbtGreen) * gx[x][y]);
                    gx_sumblue += ((image[i + k][j + l].rgbtBlue) * gx[x][y]);

                    // Gy sum
                    gy_sumred += ((image[i + k][j + l].rgbtRed) * gy[x][y]);
                    gy_sumgreen += ((image[i + k][j + l].rgbtGreen) * gy[x][y]);
                    gy_sumblue += ((image[i + k][j + l].rgbtBlue) * gy[x][y]);
                }
            }

            // sobel algo cal
            a[i][j] = round(sqrt(gx_sumred * gx_sumred + gy_sumred * gy_sumred));
            if (a[i][j] > 255)
            {
                a[i][j] = 255;
            }

            b[i][j] = round(sqrt(gx_sumgreen * gx_sumgreen + gy_sumgreen * gy_sumgreen));
            if (b[i][j] > 255)
            {
                b[i][j] = 255;ss
            }

            c[i][j] = round(sqrt(gx_sumblue * gx_sumblue + gy_sumblue * gy_sumblue));
            if (c[i][j] > 255)
            {
                c[i][j] = 255;
            }
        }
    }

    // assign new value
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = a[i][j];
            image[i][j].rgbtGreen = b[i][j];
            image[i][j].rgbtBlue = c[i][j];
        }
    }
    return;
}