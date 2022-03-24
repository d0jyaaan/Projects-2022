-- Keep a log of any SQL queries you execute as you solve the mystery.

-- find description and details of the crime
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = 'Chamberlin Street';
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
-- Interviews were conducted today with three witnesses who were present at the time —
-- each of their interview transcripts mentions the courthouse.


-- interviews
SELECT transcript
FROM interviews
WHERE month = 7 AND day = 28;


-- Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away.
-- get the license plate
SELECT minute, activity, license_plate
FROM courthouse_security_logs
WHERE month = 7 AND day = 28
AND hour = 10;
-- 16 | exit | 5P2BI95
-- 18 | exit | 94KL13X
-- 18 | exit | 6P58WS2
-- 19 | exit | 4328GD8
-- 20 | exit | G412CB7
-- 21 | exit | L93JTIZ
-- 23 | exit | 322W7JE
-- 23 | exit | 0NTHK55

-- I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money
--  get the details of ppl withdrawing money
-- I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
SELECT id
FROM passengers JOIN flights ON passengers.flight_id = flights.id
WHERE origin_airport_id IN
(SELECT id
FROM airports
WHERE city LIKE 'Fiftyville')
AND month = 7 AND day = 29
ORDER BY hour, minute
LIMIT 1;
-- 36


SELECT name
FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE person_id IN (SELECT person_id
FROM bank_accounts
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28
AND atm_location = 'Fifer Street'
AND transaction_type = 'withdraw'))
AND license_plate IN (SELECT license_plate
FROM courthouse_security_logs
WHERE month = 7 AND day = 28
AND hour = 10
AND minute > 15
AND minute < 30)

INTERSECT

SELECT name
FROM people
WHERE passport_number IN
(SELECT passport_number
FROM passengers
WHERE flight_id = 36);

-- possible suspects
-- account_number | person_id | name      | phone_number   | passport_number | license_plate
-- 49610011       | 686048    | Ernest    | (367) 555-5533 | 5773159633      | 94KL13X
-- 28500762       | 467400    | Danielle  | (389) 555-5198 | 8496433585      | 4328GD8

-- flight destination
SELECT city
FROM airports
WHERE id IN
(SELECT destination_airport_id
FROM passengers JOIN flights ON passengers.flight_id = flights.id
WHERE passport_number = 5773159633
AND month = 7 AND day = 29);

-- The thief then asked the person on the other end of the phone to purchase the flight ticket

SELECT name
FROM people
WHERE phone_number IN
(SELECT receiver
FROM phone_calls
WHERE caller = '(367) 555-5533'
AND month = 7 AND day = 28
AND duration < 60);
