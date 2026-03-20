import pymysql
from app.config import USER, PASSWORD, HOST, DB_NAME

def migrate():
    print(f"Migrando banco {DB_NAME}...")
    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
            autocommit=True
        )
        with connection.cursor() as cursor:
            try:
                cursor.execute("ALTER TABLE entregaveis ADD COLUMN ordem INT DEFAULT 0;")
                print("✅ Coluna 'ordem' adicionada com sucesso!")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print("ℹ️ Coluna 'ordem' já existe.")
                else:
                    print(f"❌ Erro ao adicionar coluna: {e}")
        connection.close()
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    migrate()
