import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()


question = cursor.execute('SELECT * FROM Question WHERE id=3').fetchall()
print(question)

answers = cursor.execute('SELECT * FROM Answer WHERE question_id=3').fetchall()
print(answers)

conn.commit()
conn.close()
