USER admin omnisci {

CREATE TEMPORARY TABLE trips (
    trip_id BIGINT,
    vendor_id TEXT ENCODING NONE,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    store_and_fwd_flag TEXT ENCODING NONE,
    rate_code_id SMALLINT,
    pickup_longitude DOUBLE,
    pickup_latitude DOUBLE,
    dropoff_longitude DOUBLE,
    dropoff_latitude DOUBLE,
    passenger_count SMALLINT,
    trip_distance DOUBLE,
    fare_amount DOUBLE,
    extra DOUBLE,
    mta_tax DOUBLE,
    tip_amount DOUBLE,
    tolls_amount DOUBLE,
    ehail_fee DOUBLE,
    improvement_surcharge DOUBLE,
    total_amount DOUBLE,
    payment_type TEXT ENCODING NONE,
    trip_type TINYINT,
    pickup TEXT ENCODING NONE,
    dropoff TEXT ENCODING NONE,
    cab_type TEXT,
    precipitation DOUBLE,
    snow_depth SMALLINT,
    snowfall DOUBLE,
    max_temperature SMALLINT,
    min_temperature SMALLINT,
    average_wind_speed DOUBLE,
    pickup_nyct2010_gid BIGINT,
    pickup_ctlabel DOUBLE,
    pickup_borocode INT,
    pickup_boroname TEXT ENCODING NONE,
    pickup_ct2010 INT,
    pickup_boroct2010 INT,
    pickup_cdeligibil TEXT ENCODING NONE,
    pickup_ntacode TEXT ENCODING NONE,
    pickup_ntaname TEXT ENCODING NONE,
    pickup_puma INT,
    dropoff_nyct2010_gid BIGINT,
    dropoff_ctlabel DOUBLE,
    dropoff_borocode BIGINT,
    dropoff_boroname TEXT ENCODING NONE,
    dropoff_ct2010 INT,
    dropoff_boroct2010 INT,
    dropoff_cdeligibil TEXT ENCODING NONE,
    dropoff_ntacode TEXT ENCODING NONE,
    dropoff_ntaname TEXT ENCODING NONE,
    dropoff_puma INT
) WITH (storage_type='CSV:trips-header-200.csv', fragment_size=2500000);

SELECT cab_type, count(*) FROM trips GROUP BY cab_type;
SELECT cab_type, count(*) FROM trips GROUP BY cab_type;
SELECT cab_type, count(*) FROM trips GROUP BY cab_type;

SELECT passenger_count, avg(total_amount) FROM trips GROUP BY passenger_count;
SELECT passenger_count, avg(total_amount) FROM trips GROUP BY passenger_count;
SELECT passenger_count, avg(total_amount) FROM trips GROUP BY passenger_count;

SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, count(*) FROM trips GROUP BY passenger_count, pickup_year;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, count(*) FROM trips GROUP BY passenger_count, pickup_year;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, count(*) FROM trips GROUP BY passenger_count, pickup_year;

SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, cast(trip_distance as int) AS distance, count(*) AS the_count FROM trips GROUP BY passenger_count, pickup_year, distance ORDER BY pickup_year, the_count desc;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, cast(trip_distance as int) AS distance, count(*) AS the_count FROM trips GROUP BY passenger_count, pickup_year, distance ORDER BY pickup_year, the_count desc;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, cast(trip_distance as int) AS distance, count(*) AS the_count FROM trips GROUP BY passenger_count, pickup_year, distance ORDER BY pickup_year, the_count desc;

SELECT cab_type, count(*) FROM trips GROUP BY cab_type;
SELECT cab_type, count(*) FROM trips GROUP BY cab_type;
SELECT cab_type, count(*) FROM trips GROUP BY cab_type;

SELECT passenger_count, avg(total_amount) FROM trips GROUP BY passenger_count;
SELECT passenger_count, avg(total_amount) FROM trips GROUP BY passenger_count;
SELECT passenger_count, avg(total_amount) FROM trips GROUP BY passenger_count;

SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, count(*) FROM trips GROUP BY passenger_count, pickup_year;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, count(*) FROM trips GROUP BY passenger_count, pickup_year;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, count(*) FROM trips GROUP BY passenger_count, pickup_year;

SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, cast(trip_distance as int) AS distance, count(*) AS the_count FROM trips GROUP BY passenger_count, pickup_year, distance ORDER BY pickup_year, the_count desc;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, cast(trip_distance as int) AS distance, count(*) AS the_count FROM trips GROUP BY passenger_count, pickup_year, distance ORDER BY pickup_year, the_count desc;
SELECT passenger_count, extract(year from pickup_datetime) AS pickup_year, cast(trip_distance as int) AS distance, count(*) AS the_count FROM trips GROUP BY passenger_count, pickup_year, distance ORDER BY pickup_year, the_count desc;

}
