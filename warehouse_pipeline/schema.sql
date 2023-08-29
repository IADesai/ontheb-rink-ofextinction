CREATE DATABASE plant_data;
\c plant_data


CREATE TABLE IF NOT EXISTS sunlight (
    sunlight_id SERIAL PRIMARY KEY,
    s_description text NOT NULL
);


CREATE TABLE IF NOT EXISTS cycle (
    cycle_id SERIAL PRIMARY KEY,
    cycle_name text
);


CREATE TABLE IF NOT EXISTS botanist (
    botanist_id SERIAL PRIMARY KEY,
    b_name text NOT NULL,
    b_email text NOT NULL,
    b_phone SMALLINT NOT NULL
);


CREATE TABLE plant (
    species_id SERIAL PRIMARY KEY,
    temperature FLOAT,
    soil_moisture FLOAT,
    humidity FLOAT,
    last_watered TIMESTAMP,
    recording_taken TIMESTAMP NOT NULL,
    sunlight_id SMALLINT,
    botanist_id SMALLINT, 
    cycle_id SMALLINT,
    CONSTRAINT fk_sunlight_id
        FOREIGN KEY(sunlight_id)
            REFERENCES sunlight(sunlight_id),
    CONSTRAINT fk_botanist_id
        FOREIGN KEY(botanist_id)
            REFERENCES botanist(botanist_id),
    CONSTRAINT fk_cycle_id
        FOREIGN KEY(cycle_id)
            REFERENCES cycle(cycle_id)
);


CREATE TABLE IF NOT EXISTS species (
    species_name_id SERIAL PRIMARY KEY,
    scientific_name text NOT NULL UNIQUE,
    species_id SMALLINT NOT NULL UNIQUE
    CONSTRAINT fk_species_id
        FOREIGN KEY(species_id)
            REFERENCES plant(species_id)
);




