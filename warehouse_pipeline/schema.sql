CREATE DATABASE plants;
\c plants


CREATE TABLE IF NOT EXISTS stories (
    id SERIAL PRIMARY KEY,
    title text NOT NULL UNIQUE,
    url text NOT NULL UNIQUE,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


INSERT INTO stories(title, url, created_at, updated_at) VALUES ('Actor released from prison in sex-trafficking case', 'https://www.bbc.co.uk/news/world-us-canada-66111026', '2023-07-06 13:38:33.238446', '2023-07-06 13:38:33.238446');
INSERT INTO stories(title, url, created_at, updated_at) VALUES ('Adele speaks out against audiences throwing objects on stage', 'https://www.bbc.co.uk/news/newsbeat-66108108', '2023-07-06 13:38:33.238922', '2023-07-06 13:38:33.238922');
INSERT INTO stories(title, url, created_at, updated_at) VALUES ('"I want more people to feel like this is a sport for them"', 'https://www.bbc.co.uk/sport/diving/66093123', '2023-07-06 13:38:33.240815', '2023-07-06 13:38:33.240815');


CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    direction text DEFAULT 'up'::text NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    story_id INT,
    CONSTRAINT fk_story_id
        FOREIGN KEY(story_id)
            REFERENCES stories(id)
);




