/*
 Завдання на SQL до лекції 03.
 */

/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT COUNT(fc.film_id) AS total_films, c.name AS category
FROM film_category AS fc
    LEFT JOIN category AS c ON c.category_id = fc.category_id
GROUP BY c.name
ORDER BY total_films DESC;

/*
 total_films |  category
-------------+-------------
          74 | Sports
          73 | Foreign
          69 | Family
          68 | Documentary
          66 | Animation
          64 | Action
          63 | New
          62 | Drama
          61 | Sci-Fi
          61 | Games
          60 | Children
          58 | Comedy
          57 | Travel
          57 | Classics
          56 | Horror
          51 | Music
(16 rows)
*/

/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
WITH top_rental_films_actors AS (
    SELECT i.film_id, COUNT(i.film_id) AS rental_count, fa.actor_id
    FROM rental AS r
        LEFT JOIN inventory AS i ON i.inventory_id = r.inventory_id
        LEFT JOIN film_actor AS fa ON fa.film_id = i.film_id
    GROUP BY i.film_id, fa.actor_id
    ORDER BY rental_count DESC
)
SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor
FROM top_rental_films_actors AS trfa
    LEFT JOIN actor AS a ON a.actor_id = trfa.actor_id
LIMIT 10;

/*
       actor
-------------------
 RIP CRAWFORD
 GARY PHOENIX
 CHARLIZE DENCH
 TIM HACKMAN
 KIRSTEN AKROYD
 BURT TEMPLE
 JAYNE SILVERSTONE
 JUDY DEAN
 TOM MIRANDA
 WARREN JACKMAN
(10 rows)
*/

/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
WITH payment_by_category AS (
    SELECT SUM(p.amount) AS total, c.name
    FROM payment AS p
        LEFT JOIN rental AS r ON r.rental_id = p.rental_id
        LEFT JOIN inventory AS i ON i.inventory_id = r.inventory_id
        LEFT JOIN film_category AS fc ON fc.film_id = i.film_id
        LEFT JOIN category AS c ON c.category_id = fc.category_id
    GROUP BY c.name
)
SELECT pbc.name AS category
FROM payment_by_category AS pbc
WHERE pbc.total = (
    SELECT MAX(pbc.total)
    FROM payment_by_category AS pbc
);

/*
 category
----------
 Sports
(1 row)
*/

/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT f.title
FROM film AS f
LEFT JOIN inventory AS i ON f.film_id = i.film_id
WHERE i.film_id IS NULL;

/*
         title
------------------------
 ALICE FANTASIA
 APOLLO TEEN
 ARGONAUTS TOWN
 ARK RIDGEMONT
 ARSENIC INDEPENDENCE
 BOONDOCK BALLROOM
 BUTCH PANTHER
 CATCH AMISTAD
 CHINATOWN GLADIATOR
 CHOCOLATE DUCK
 COMMANDMENTS EXPRESS
 CROSSING DIVORCE
 CROWDS TELEMARK
 CRYSTAL BREAKING
 DAZED PUNK
 DELIVERANCE MULHOLLAND
 FIREHOUSE VIETNAM
 FLOATS GARDEN
 FRANKENSTEIN STRANGER
 GLADIATOR WESTWARD
 GUMP DATE
 HATE HANDICAP
 HOCUS FRIDA
 KENTUCKIAN GIANT
 KILL BROTHERHOOD
 MUPPET MILE
 ORDER BETRAYED
 PEARL DESTINY
 PERDITION FARGO
 PSYCHO SHRUNK
 RAIDERS ANTITRUST
 RAINBOW SHOCK
 ROOF CHAMPION
 SISTER FREDDY
 SKY MIRACLE
 SUICIDES SILENCE
 TADPOLE PARK
 TREASURE COMMAND
 VILLAIN DESPERATE
 VOLUME HOUSE
 WAKE JAWS
 WALLS ARTIST
(42 rows)
*/

/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
WITH children_category_films AS (
	SELECT fc.film_id
	FROM film_category AS fc
	    LEFT JOIN category AS c ON c.category_id = fc.category_id
	WHERE c.name = 'Children'
),
filmography_of_actor AS (
    SELECT fa.actor_id, COUNT(ccf.film_id) AS total_films
    FROM children_category_films AS ccf
        LEFT JOIN film_actor AS fa ON fa.film_id = ccf.film_id
    GROUP BY fa.actor_id
    ORDER BY total_films DESC
)
SELECT CONCAT(a.first_name, ' ', a.last_name) AS actor
FROM filmography_of_actor AS foa
    LEFT JOIN actor AS a ON a.actor_id = foa.actor_id
LIMIT 3;

/*
        actor
---------------------
 PENELOPE GUINESS
 NICK WAHLBERG
 JOHNNY LOLLOBRIGIDA
(3 rows)
*/