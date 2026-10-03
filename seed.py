from backend.app.models.database import init_db, seed_db


def main():
    print("Initializing database tables...")
    init_db()
    print("Seeding database data...")
    seed_db()
    print("Database setup complete.")


if __name__ == "__main__":
    main()