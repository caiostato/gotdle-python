import psycopg2
from psycopg2 import sql

import os
from dotenv import load_dotenv

import json

load_dotenv()

def main():
  connection = connect_db()
  try:
    insert_characters(connection)
  except Exception as e:
    print(f"Error inserting characters into the database: {e}")
  finally:
    if connection:
        connection.close()
        print("Database connection closed.")


def connect_db():
  connection = None
  try:
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port = os.getenv('DB_PORT')
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Connected to PostgreSQL Database. Version: {db_version[0]}")

  except Exception as e:
    print(f"Error connecting to the database: {e}")

  finally:
    if connection:
        cursor.close()
        return connection

def insert_characters (connection) :
  with open('characters.json', 'r') as file:
    data = json.load(file)

  insert_query = """
  INSERT INTO characters (name, gender, origin, house, first_season, marriage_count, siblings, children)
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
  """

  for character in data:
    character_data = (
        character.get('name', ''),
        character.get('gender', 'Unknown'),
        character.get('origin', 'Unknown'),
        character.get('house', 'Unknown'),
        character.get('first_season', 0),
        character.get('marriage_count', 0),  # Ensure the key is 'marriage_count' not 'marriege_count'
        character.get('siblings', 0),
        character.get('children', 0),
    )
    
    print(character_data)
    try:
      cursor = connection.cursor()
      cursor.execute(insert_query, character_data)
      connection.commit()
      print(f"Inserted {character['name']} successfully!")
    except Exception as e:
      print(f"Error inserting data: {e}")
    finally:
      if connection:
        cursor.close()

        print("Connection cursor closed.")

    print("Data inserted successfully!")

if __name__ == '__main__':
    main()