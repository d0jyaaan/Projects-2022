-- list the names of all people who starred in a movie released in 2004, ordered by birth year
-- those who do have a birth year are listed in order.
-- If a person appeared in more than one movie in 2004, they should only appear in your results once

SELECT DISTINCT name
FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON stars.movie_id = movies.id
WHERE year = 2004
ORDER BY birth, name ASC;