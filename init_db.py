import pymysql
from app.config import USER, PASSWORD, HOST, DB_NAME

def seed_db():
    print(f"Semeando dados de teste no banco {DB_NAME}...")
    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
            autocommit=True
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            
            # Create Table Entregaveis Modelo (if not handled by migrations)
            print("Garantindo tabela entregaveis_modelo...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entregaveis_modelo (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(255) UNIQUE NOT NULL
                ) ENGINE=InnoDB;
            """)
            
            # Seed Admins
            print("Inserindo Admins...")
            cursor.execute("INSERT IGNORE INTO administradores (nomeAdmin, emailAdmin, senhaAdmin) VALUES ('Rafael Timóteo', 'rafael@gmail.com', 'gamer'), ('admin', 'adm@adm', 'adm');")
            
            # Seed Mentorias
            print("Inserindo Mentorias...")
            cursor.execute("INSERT IGNORE INTO mentorias (id, nome, descricao, data_create) VALUES (1, 'Mentoria MPS', 'Metodologia de Produtividade e Sucesso', '2025-01-01'), (2, 'Mentoria DOP', 'Direcionamento e Otimização de Processos', '2025-01-05');")
            
            # Seed Entregáveis (Templates)
            print("Inserindo Templates de Entregáveis...")
            cursor.executemany("INSERT IGNORE INTO entregaveis (id, id_mentoria, nome) VALUES (%s, %s, %s)", [
                (1, 1, 'Assinar Contrato MPS'),
                (2, 1, 'Acesso ao Portal do Aluno'),
                (3, 1, 'Primeira Chamada de Onboarding'),
                (4, 2, 'Diagnóstico Empresarial DOP'),
                (5, 2, 'Configuração de Ferramentas'),
                (6, 2, 'Sessão de Alinhamento Estratégico')
            ])

            # Seed Entregáveis Modelo (Pool Global)
            print("Inserindo Pool Global de Entregáveis...")
            cursor.executemany("INSERT IGNORE INTO entregaveis_modelo (nome) VALUES (%s)", [
                ('Logo',), ('Site',), ('Protótipo',), ('Projeto Final',),
                ('Assinar Contrato',), ('Onboarding',), ('Diagnóstico',)
            ])
            
            # Seed Alunos
            print("Inserindo Alunos...")
            cursor.execute("INSERT IGNORE INTO alunos (id, nomeAluno, emailAluno, senhaAluno, CPFAluno, mentoria_id) VALUES (1, 'João Aluno Teste', 'joao@teste.com', '123', '123.456.789-00', 1), (2, 'Maria Aluna Teste', 'maria@teste.com', '123', '987.654.321-11', 2);")
            
            # Seed Status de Entregáveis
            print("Inserindo Status de Entregáveis...")
            cursor.executemany("INSERT IGNORE INTO alunos_entregaveis (aluno_id, entregavel_id, status, data_entrega) VALUES (%s, %s, %s, %s)", [
                (1, 1, 'Entregue', '2025-01-10'),
                (1, 2, 'Pendente', None),
                (1, 3, 'Pendente', None),
                (2, 4, 'Em Andamento', None),
                (2, 5, 'Pendente', None),
                (2, 6, 'Pendente', None)
            ])
            
            # Seed Reuniões (id_aluno, id_mentoria)
            print("Inserindo Reuniões...")
            cursor.execute("INSERT IGNORE INTO reunioes (id, id_aluno, id_mentoria, nome, data) VALUES (1, 1, 1, 'Onboarding João', '2025-01-12'), (2, 2, 2, 'Kickoff Maria', '2025-01-15');")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            print("✅ Dados de teste inseridos com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro ao semear o banco de dados: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    seed_db()
