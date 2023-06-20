CREATE TABLE Places (
  place_id INTEGER PRIMARY KEY,
  name TEXT,
  latitude REAL,
  longitude REAL
);

CREATE TABLE People (
  person_id INTEGER PRIMARY KEY,
  name TEXT,
  birth_date DATE,
  birth_place_id INTEGER,
  FOREIGN KEY (birth_place_id) REFERENCES Places(place_id)
);

CREATE TABLE Technology (
  tech_id INTEGER PRIMARY KEY,
  name TEXT,
  description TEXT
);

CREATE TABLE Dates (
  date_id INTEGER PRIMARY KEY,
  event_date DATE,
  description TEXT
);

CREATE TABLE Projects (
  project_id INTEGER PRIMARY KEY,
  name TEXT,
  start_date_id INTEGER,
  end_date_id INTEGER,
  FOREIGN KEY (start_date_id) REFERENCES Dates(date_id),
  FOREIGN KEY (end_date_id) REFERENCES Dates(date_id)
);

CREATE TABLE Project_People (
  project_id INTEGER,
  person_id INTEGER,
  FOREIGN KEY (project_id) REFERENCES Projects(project_id),
  FOREIGN KEY (person_id) REFERENCES People(person_id)
);

CREATE TABLE Project_Technology (
  project_id INTEGER,
  tech_id INTEGER,
  FOREIGN KEY (project_id) REFERENCES Projects(project_id),
  FOREIGN KEY (tech_id) REFERENCES Technology(tech_id)
);

CREATE TABLE Project_Places (
  project_id INTEGER,
  place_id INTEGER,
  FOREIGN KEY (project_id) REFERENCES Projects(project_id),
  FOREIGN KEY (place_id) REFERENCES Places(place_id)
);

INSERT INTO Places (name, latitude, longitude) VALUES ('Los Alamos, New Mexico', 35.8789, -106.3035);
INSERT INTO Places (name, latitude, longitude) VALUES ('Oak Ridge, Tennessee', 35.9417, -84.3106);
INSERT INTO Places (name, latitude, longitude) VALUES ('Hanford Site, Washington', 46.6467, -119.5400);
INSERT INTO Places (name, latitude, longitude) VALUES ('Chicago, Illinois', 41.8781, -87.6298);
INSERT INTO Places (name, latitude, longitude) VALUES ('Alamogordo, New Mexico', 32.8998, -105.9603);
INSERT INTO Places (name, latitude, longitude) VALUES ('Washington, D.C.', 38.9072, -77.0379);
INSERT INTO Places (name, latitude, longitude) VALUES ('Wendover Airfield, Utah', 40.7391, -113.9557);
INSERT INTO Places (name, latitude, longitude) VALUES ('Hiroshima, Japan', 34.3853, 132.4553);
INSERT INTO Places (name, latitude, longitude) VALUES ('Nagasaki, Japan', 32.7503, 129.8777);

INSERT INTO People (name, birth_date, birth_place_id) VALUES ('J. Robert Oppenheimer', '1904-04-22', 7);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Leslie Groves', '1896-08-17', 13);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Enrico Fermi', '1901-09-29', 14);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Niels Bohr', '1885-10-07', 15);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Richard Feynman', '1918-05-11', 7);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Edward Teller', '1908-01-15', 16);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Ernest Lawrence', '1901-08-08', 17);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Vannevar Bush', '1890-03-11', 18);
INSERT INTO People (name, birth_date, birth_place_id) VALUES ('Klaus Fuchs', '1911-12-29', 19);

INSERT INTO Dates (event_date, description) VALUES ('1939-08-02', 'Albert Einstein writes letter to President Roosevelt, warning about the potential for atomic weapons');
INSERT INTO Dates (event_date, description) VALUES ('1941-12-07', 'Attack on Pearl Harbor');
INSERT INTO Dates (event_date, description) VALUES ('1942-06-28', 'Manhattan Project officially established');
INSERT INTO Dates (event_date, description) VALUES ('1942-12-02', 'First controlled nuclear chain reaction (Chicago Pile-1)');
INSERT INTO Dates (event_date, description) VALUES ('1945-07-16', 'Trinity Test (First atomic bomb detonation)');
INSERT INTO Dates (event_date, description) VALUES ('1945-08-06', 'Atomic bombing of Hiroshima');
INSERT INTO Dates (event_date, description) VALUES ('1945-08-09', 'Atomic bombing of Nagasaki');
INSERT INTO Dates (event_date, description) VALUES ('1945-08-14', 'Japanese government indicates willingness to surrender');
INSERT INTO Dates (event_date, description) VALUES ('1945-08-15', 'Japan surrenders (V-J Day)');
INSERT INTO Dates (event_date, description) VALUES ('1945-10-24', 'United Nations officially established');

select event_date, STRFTIME("%Y", event_date) year, STRFTIME("%W", event_date) + 1 week, count(*) events
from dates 
group by STRFTIME("%Y", event_date), STRFTIME("%W", event_date)

select STRFTIME("%Y", event_date) year, count(event_date) events
from dates
group by STRFTIME("%Y", event_date)

select event_date, description, length(description), length(desc_long) 
from dates
order by event_date 

select description, count(description) from dates
group by description 
order by description 

select STRFTIME("%W", "1947-01-01") + 1 week

select p.name 
from dates d, people p
where p.name  in 
(select d.desc_long from dates d) 

select p.name, p.join_date, d.description 
from dates d, people p
where p.join_date = d.event_date 

select cx, cy, round(cx, 2), round(cy, 2) from places

update places set cx = round(cx, 2), cy = round(cy, 2)

INSERT INTO people (name, description, birth_date)
VALUES ('Klaus Fuchs', 'aKlaus Fuchs was a German-born physicist who worked on the Manhattan Project and provided classified information about atomic weapons to the Soviet Union.', '1911-12-29');

INSERT INTO people (name, description, birth_date)
VALUES ('Julius Rosenberg', 'Julius Rosenberg was an American electrical engineer and a key figure in the Soviet atomic espionage network. He and his wife, Ethel Rosenberg, were involved in transmitting classified information about the atomic bomb to the Soviet Union.', '1918-05-12');

INSERT INTO people (name, description, birth_date)
VALUES ('Ethel Rosenberg', 'Ethel Rosenberg was an American activist who, along with her husband, Julius Rosenberg, participated in transmitting classified information about the atomic bomb to the Soviet Union.', '1915-09-28');

INSERT INTO people (name, description, birth_date)
VALUES ('Theodore Hall', 'Theodore Hall was an American physicist who worked on the Manhattan Project and passed classified information about the atomic bomb to the Soviet Union. He was the youngest scientist to work on the project.', '1925-10-20');

INSERT INTO people (name, description, birth_date)
VALUES ('David Greenglass', 'David Greenglass was an American machinist and former soldier who worked on the Manhattan Project. He provided classified information about atomic bomb designs to his brother-in-law, Julius Rosenberg, who passed it to the Soviet Union.', '1922-03-02');

INSERT INTO people (name, description, birth_date)
VALUES ('Morris Cohen', 'Morris Cohen, also known as "Agent Lattimore," was an American spy who worked as a courier for Soviet intelligence.', NULL);

INSERT INTO people (name, description, birth_date)
VALUES ('Harry Gold', 'Harry Gold was an American laboratory chemist who acted as a courier for Soviet atomic spies, including passing information about the Manhattan Project to the Soviet Union.', '1910-12-11');

INSERT INTO people (name, description, birth_date)
VALUES ('George Koval', 'George Koval was a Soviet intelligence officer and American-born physicist who infiltrated the Manhattan Project and provided valuable information to the Soviet Union.', '1913-12-25');

INSERT INTO people (name, description, birth_date)
VALUES ('Irving Lerner', 'Irving Lerner was an American film director and screenwriter. There is no evidence suggesting his involvement in atomic espionage.', NULL);

INSERT INTO people (name, description, birth_date)
VALUES ('Alan Nunn May', 'Alan Nunn May was a British physicist who worked on the Manhattan Project and provided classified information to the Soviet Union.', '1911-05-24');

INSERT INTO people (name, description, birth_date)
VALUES ('Saville Sax', 'Saville Sax was an American chemist who worked on the Manhattan Project and was involved in espionage activities for the Soviet Union.', NULL);

INSERT INTO people (name, description, birth_date)
VALUES ('Oscar Seborer', 'Oscar Seborer was an American electrical engineer who participated in Soviet atomic espionage during the Manhattan Project.', NULL);

INSERT INTO people (name, description, birth_date)
VALUES ('Morton Sobell', 'Morton Sobell was an American engineer who was involved in passing atomic-related information to the Soviet Union during the Manhattan Project.', '1917-04-11');

INSERT INTO people (name, description, birth_date)
VALUES ('Melita Norwood', 'Melita Norwood was a British secretary who, during World War II, passed atomic secrets to the Soviet Union. She continued her espionage activities even after the war.', '1912-03-25');

INSERT INTO people (name, description, birth_date)
VALUES ('Arthur Adams', 'Arthur Adams was an American machinist who worked on the Manhattan Project and later provided classified information to the Soviet Union.', NULL);

CREATE TABLE Buildings (
  building_id INT PRIMARY KEY,
  name VARCHAR(255),
  place_id INT,
  FOREIGN KEY (place_id) REFERENCES Places(place_id)
);

ALTER TABLE buildings
ADD coords_polygon polygon;

ALTER TABLE buildings
ADD coords_text TEXT;

SELECT load_extension("mod_spatialite.so")

SELECT load_extension("mod_spatialite");

select spatialite_version()

select spatialite_target_cpu()

select geos_version()

select HasGeoCallbacks()

select AsWKT(ST_LineFromText(b.coords_text)) from Buildings b  

select AsWKT(b.coords_text) from Buildings b  

select AsText(Envelope(b.coords_polygon)) from Buildings b  

select b.building_id, ST_AsText(coords_text), GeometryType(b.coords_polygon) from Buildings b 

update Places set workers =
ABS(RANDOM())%(8500-250) + 250
where workers IS NULL
