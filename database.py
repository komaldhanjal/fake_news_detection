import mysql.connector

# ===============================
# Database connection
# ===============================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",   
        database="fake_news_db"       
    )

# ===============================
# Insert prediction data
# ===============================
def insert_prediction(news_text, result, confidence):
    db = get_connection()
    my_cursor = db.cursor()

    query = """
        INSERT INTO asd (news_text, result, confidence)
        VALUES (%s, %s, %s)
    """
    values = (news_text, result, confidence)

    my_cursor.execute(query, values)
    db.commit()

    my_cursor.close()
    db.close()

# ===============================
# Fetch all predictions (optional)
# ===============================
def fetch_all_predictions():
    db = get_connection()
    my_cursor = db.cursor()

    my_cursor.execute("SELECT id, news_text, result, confidence, created_at FROM asd ORDER BY id DESC")
    data = my_cursor.fetchall()

    my_cursor.close()
    db.close()
    return data



# ===============================
# Test (optional – sirf check ke liye)
# ===============================
if __name__ == "__main__":
    insert_prediction(
        "India launches new AI policy",
        "Real",
        91.2
    )

    records = fetch_all_predictions()
    for row in records:
        print(row)
