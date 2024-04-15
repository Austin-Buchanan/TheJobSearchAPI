import psycopg2
from config import load_config

def create_tables():
    """Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE main_applications (
            application_id SERIAL PRIMARY KEY, 
            employer_name VARCHAR(255) NOT NULL,
            job_name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            application_date DATE,
            status VARCHAR(255),
            link_for_updates TEXT, 
            notes TEXT
        )
        """,
        """
        CREATE TABLE safety_nets (
            application_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(255) NOT NULL,
            job_name VARCHAR(255) NOT NULL,
            shift_type VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            application_date DATE,
            status VARCHAR(255),
            link_for_updates TEXT,
            notes TEXT
        )
        """,
        """
        CREATE TABLE employer_search (
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(255) NOT NULL,
            date_searched DATE,
            has_openings VARCHAR(127),
            page_link TEXT
        )
        """
    )

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()