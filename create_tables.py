#!/usr/bin/env python3
"""Script to create database tables"""

from src.database.core import engine, Base, DATABASE_URL
from src.entities.todo import Todo
from src.entities.user import User

print(f"Database URL: {DATABASE_URL}")
print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
print("\nTables:")
for table in Base.metadata.sorted_tables:
    print(f"  - {table.name}")

