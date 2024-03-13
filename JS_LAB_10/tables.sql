CREATE TABLE if not exists Stations (station_id INT PRIMARY KEY,station_name VARCHAR(255));

CREATE TABLE if not exists Rentals (rental_id INT PRIMARY KEY,bike_number INT,start_time TIMESTAMP,end_time TIMESTAMP,rental_station INT REFERENCES Stations(station_id),return_station INT REFERENCES Stations(station_id));
