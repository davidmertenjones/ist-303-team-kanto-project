DROP TABLE IF EXISTS lacounty;

CREATE TABLE lacounty (
    fac_id TEXT PRIMARY KEY,
    fac_name TEXT NOT NULL,
    "address" TEXT NOT NULL,
    city TEXT NOT NULL,
    "state" TEXT NOT NULL,
    zip_code INTEGER NOT NULL,
    county TEXT NOT NULL,
    tel_num TEXT NOT NULL,
    hosp_type TEXT NOT NULL,
    hosp_owner TEXT NOT NULL,
    "emergency" TEXT NOT NULL,
    birth_friendly TEXT NOT NULL,
    rating INTEGER NOT NULL

);
