import psycopg2
from config import load_config

def create_tables():
    """Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE main_applications (
            app_id SERIAL PRIMARY KEY, 
            employer_name VARCHAR(255) NOT NULL,
            job_name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            app_date DATE,
            status VARCHAR(255),
            update_link TEXT, 
            notes TEXT,
            maint_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE UNIQUE INDEX main_app_index
        ON main_applications (employer_name, job_name, location, app_date);
        """,
        """
        CREATE TABLE safety_nets (
            app_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(255) NOT NULL,
            job_name VARCHAR(255) NOT NULL,
            shift_type VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            app_date DATE,
            status VARCHAR(255),
            update_link TEXT,
            notes TEXT,
            maint_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE UNIQUE INDEX safety_net_index
        ON safety_nets (employer_name, job_name, shift_type, location, app_date);
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