// Implements a dictionary's functionality

#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int total = 0;

// Number of buckets in hash table
const unsigned int N = (45) * ('z') * ('z');

// Hash table
node *table[N];


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int hashvalue = hash(word);
    node *cursor = table[hashvalue];

    // compare word with the one in hashtable
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}


// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int sum = 0;
    int length = strlen(word);
    char temp[length];

    for (int i = 0; i < strlen(word); i++)
    {
        temp[i] = tolower(word[i]);
    }

    // calculate hashvalue
    if (length > 1)
    {
        sum += (length * temp[0] * temp[1]);
    }
    else
    {
        sum += temp[0];
    }
    // return
    return (sum);
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    FILE *DICTIONARY = fopen(dictionary, "r");
    // error checking
    if (DICTIONARY == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    // read every word and create hash
    while (fscanf(DICTIONARY, "%s", word) != EOF)
    {
        node *newnode = malloc(sizeof(node));
        // if malloc error or null
        if (newnode == NULL)
        {
            return false;
        }
        // copy word into newnode
        strcpy(newnode->word, word);
        newnode->next = NULL;

        // using a hash function
        int index = hash(word);

        // if theres nothing at table[index]
        // assign newnode to it
        if (table[index] == NULL)
        {
            table[index] = newnode;
        }
        else
        {
            // if theres a node at table[index]
            // assign table[index] as newnode->next
            // change table[index] to newnode
            // newnode-> _ -> _ (linked list)
            newnode->next = table[index];
            table[index] = newnode;
        }
        // increase size for each word
        total++;
    }
    fclose(DICTIONARY);
    return true;
}



// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return total;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *header = table[i];
        node *cursor = header;
        node *tmp = header;

        // free
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
