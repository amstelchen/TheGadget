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

