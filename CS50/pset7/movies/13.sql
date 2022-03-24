-- list the names of all people who starred in a movie in which Kevin Bacon
-- Your query should output a table with a single column for the name of each person.
-- There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
-- Kevin Bacon himself should not be included in the resulting list

SELECT name
FROM people JOIN stars ON stars.person_id = people.id
WHERE movie_id IN
(SELECT movie_id
FROM stars JOIN people ON stars.person_id = people.id
WHERE birth = 1958 and name = 'Kevin Bacon')
AND name != 'Kevin Bacon';

