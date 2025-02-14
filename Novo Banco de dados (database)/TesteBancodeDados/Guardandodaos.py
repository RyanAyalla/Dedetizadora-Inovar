import psycopg2

try:
    conn = psycopg2.connect(
        dbname="Dedetizadora_Inovar",
        user="postgres",
        password="ryan1234",
        host="localhost",
        port="5432"
    )
    print("Banco de dados conectado com sucesso!")
    conn.close()  # Fecha a conexão após o teste
except psycopg2.Error as e:
    print("Erro ao conectar ao banco de dados:", e)