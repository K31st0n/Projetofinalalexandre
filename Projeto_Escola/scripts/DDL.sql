-- Script DDL para criação do banco de dados PostgreSQL
-- Sistema de gerenciamento escolar infantil

-- Conectar ao banco escola_db (deve ser criado previamente)
-- \c escola_db;

-- Tabela professores: Armazena informações dos professores
CREATE TABLE IF NOT EXISTS professores (
    id_professor SERIAL PRIMARY KEY,  -- Identificador único do professor (auto incremento)
    nome_completo VARCHAR(255) NOT NULL,  -- Nome completo do professor
    email VARCHAR(100),  -- E-mail de contato do professor
    telefone VARCHAR(20)  -- Telefone de contato do professor
);

-- Comentários nas colunas da tabela professores
COMMENT ON TABLE professores IS 'Tabela que armazena informações dos professores';
COMMENT ON COLUMN professores.id_professor IS 'Identificador único do professor';
COMMENT ON COLUMN professores.nome_completo IS 'Nome completo do professor';
COMMENT ON COLUMN professores.email IS 'E-mail de contato do professor';
COMMENT ON COLUMN professores.telefone IS 'Telefone de contato do professor';

-- Tabela turmas: Representa as turmas da escola
CREATE TABLE IF NOT EXISTS turmas (
    id_turma SERIAL PRIMARY KEY,  -- Identificador único da turma
    nome_turma VARCHAR(50) NOT NULL,  -- Nome identificador da turma
    id_professor INTEGER,  -- Professor responsável pela turma
    horario VARCHAR(100),  -- Horário de funcionamento da turma
    FOREIGN KEY (id_professor) REFERENCES professores(id_professor) ON DELETE SET NULL
);

-- Comentários nas colunas da tabela turmas
COMMENT ON TABLE turmas IS 'Tabela que representa as turmas da escola';
COMMENT ON COLUMN turmas.id_turma IS 'Identificador único da turma';
COMMENT ON COLUMN turmas.nome_turma IS 'Nome identificador da turma';
COMMENT ON COLUMN turmas.id_professor IS 'Professor responsável pela turma';
COMMENT ON COLUMN turmas.horario IS 'Horário de funcionamento da turma';

-- Tabela alunos: Armazena informações dos alunos
CREATE TABLE IF NOT EXISTS alunos (
    id_aluno SERIAL PRIMARY KEY,  -- Identificador único do aluno
    nome_completo VARCHAR(255) NOT NULL,  -- Nome completo do aluno
    data_nascimento DATE NOT NULL,  -- Data de nascimento do aluno
    id_turma INTEGER,  -- Turma à qual o aluno pertence
    nome_responsavel VARCHAR(255) NOT NULL,  -- Nome do responsável legal
    telefone_responsavel VARCHAR(20) NOT NULL,  -- Telefone do responsável
    email_responsavel VARCHAR(100),  -- E-mail do responsável
    informacoes_adicionais TEXT,  -- Informações adicionais sobre o aluno
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma) ON DELETE SET NULL
);

-- Comentários nas colunas da tabela alunos
COMMENT ON TABLE alunos IS 'Tabela que armazena informações dos alunos';
COMMENT ON COLUMN alunos.id_aluno IS 'Identificador único do aluno';
COMMENT ON COLUMN alunos.nome_completo IS 'Nome completo do aluno';
COMMENT ON COLUMN alunos.data_nascimento IS 'Data de nascimento do aluno';
COMMENT ON COLUMN alunos.id_turma IS 'Turma à qual o aluno pertence';
COMMENT ON COLUMN alunos.nome_responsavel IS 'Nome do responsável legal';
COMMENT ON COLUMN alunos.telefone_responsavel IS 'Telefone do responsável';
COMMENT ON COLUMN alunos.email_responsavel IS 'E-mail do responsável';
COMMENT ON COLUMN alunos.informacoes_adicionais IS 'Informações adicionais sobre o aluno';

-- Tabela pagamentos: Registra os pagamentos realizados
CREATE TABLE IF NOT EXISTS pagamentos (
    id_pagamento SERIAL PRIMARY KEY,  -- Identificador único do pagamento
    id_aluno INTEGER NOT NULL,  -- Aluno vinculado ao pagamento
    data_pagamento DATE NOT NULL,  -- Data em que o pagamento foi realizado
    valor_pago DECIMAL(10, 2) NOT NULL,  -- Valor do pagamento
    forma_pagamento VARCHAR(50) NOT NULL,  -- Forma de pagamento utilizada
    referencia VARCHAR(100) NOT NULL,  -- Referência/descrição do pagamento
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno) ON DELETE CASCADE
);

-- Comentários nas colunas da tabela pagamentos
COMMENT ON TABLE pagamentos IS 'Tabela que registra os pagamentos realizados';
COMMENT ON COLUMN pagamentos.id_pagamento IS 'Identificador único do pagamento';
COMMENT ON COLUMN pagamentos.id_aluno IS 'Aluno vinculado ao pagamento';
COMMENT ON COLUMN pagamentos.data_pagamento IS 'Data em que o pagamento foi realizado';
COMMENT ON COLUMN pagamentos.valor_pago IS 'Valor do pagamento';
COMMENT ON COLUMN pagamentos.forma_pagamento IS 'Forma de pagamento utilizada';
COMMENT ON COLUMN pagamentos.referencia IS 'Referência/descrição do pagamento';

-- Tabela presencas: Registra a frequência dos alunos
CREATE TABLE IF NOT EXISTS presencas (
    id_presenca SERIAL PRIMARY KEY,  -- Identificador único do registro de presença
    id_aluno INTEGER NOT NULL,  -- Aluno referenciado
    data_presenca DATE NOT NULL,  -- Data da aula/referência
    presente BOOLEAN NOT NULL,  -- Indica se o aluno estava presente
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno) ON DELETE CASCADE
);

-- Comentários nas colunas da tabela presencas
COMMENT ON TABLE presencas IS 'Tabela que registra a frequência dos alunos';
COMMENT ON COLUMN presencas.id_presenca IS 'Identificador único do registro de presença';
COMMENT ON COLUMN presencas.id_aluno IS 'Aluno referenciado';
COMMENT ON COLUMN presencas.data_presenca IS 'Data da aula/referência';
COMMENT ON COLUMN presencas.presente IS 'Indica se o aluno estava presente';

-- Tabela atividades: Armazena as atividades realizadas
CREATE TABLE IF NOT EXISTS atividades (
    id_atividade SERIAL PRIMARY KEY,  -- Identificador único da atividade
    descricao TEXT NOT NULL,  -- Descrição da atividade
    data_realizacao DATE NOT NULL  -- Data de realização da atividade
);

-- Comentários nas colunas da tabela atividades
COMMENT ON TABLE atividades IS 'Tabela que armazena as atividades realizadas';
COMMENT ON COLUMN atividades.id_atividade IS 'Identificador único da atividade';
COMMENT ON COLUMN atividades.descricao IS 'Descrição da atividade';
COMMENT ON COLUMN atividades.data_realizacao IS 'Data de realização da atividade';

-- Tabela atividade_aluno: Relacionamento muitos-para-muitos entre Atividade e Aluno
CREATE TABLE IF NOT EXISTS atividade_aluno (
    id_atividade INTEGER NOT NULL,  -- Referência à atividade
    id_aluno INTEGER NOT NULL,  -- Referência ao aluno
    PRIMARY KEY (id_atividade, id_aluno),
    FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade) ON DELETE CASCADE,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno) ON DELETE CASCADE
);

-- Comentários na tabela atividade_aluno
COMMENT ON TABLE atividade_aluno IS 'Tabela de relacionamento muitos-para-muitos entre Atividade e Aluno';
COMMENT ON COLUMN atividade_aluno.id_atividade IS 'Referência à atividade';
COMMENT ON COLUMN atividade_aluno.id_aluno IS 'Referência ao aluno';

-- Tabela usuarios: Armazena os usuários do sistema
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,  -- Identificador único do usuário
    login VARCHAR(50) UNIQUE NOT NULL,  -- Login de acesso
    senha VARCHAR(255) NOT NULL,  -- Senha criptografada
    nivel_acesso VARCHAR(20) NOT NULL,  -- Nível de acesso (admin, secretaria, professor)
    id_professor INTEGER,  -- Vínculo com professor, se aplicável
    FOREIGN KEY (id_professor) REFERENCES professores(id_professor) ON DELETE SET NULL
);

-- Comentários nas colunas da tabela usuarios
COMMENT ON TABLE usuarios IS 'Tabela que armazena os usuários do sistema';
COMMENT ON COLUMN usuarios.id_usuario IS 'Identificador único do usuário';
COMMENT ON COLUMN usuarios.login IS 'Login de acesso';
COMMENT ON COLUMN usuarios.senha IS 'Senha criptografada';
COMMENT ON COLUMN usuarios.nivel_acesso IS 'Nível de acesso (admin, secretaria, professor)';
COMMENT ON COLUMN usuarios.id_professor IS 'Vínculo com professor, se aplicável';

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_alunos_turma ON alunos(id_turma);
CREATE INDEX IF NOT EXISTS idx_pagamentos_aluno ON pagamentos(id_aluno);
CREATE INDEX IF NOT EXISTS idx_presencas_aluno ON presencas(id_aluno);
CREATE INDEX IF NOT EXISTS idx_presencas_data ON presencas(data_presenca);
CREATE INDEX IF NOT EXISTS idx_usuarios_login ON usuarios(login);

-- Dados iniciais para teste (opcional)
-- INSERT INTO professores (nome_completo, email, telefone) VALUES 
-- ('Maria Silva', 'maria@escola.com', '11999999999'),
-- ('João Santos', 'joao@escola.com', '11888888888');

-- INSERT INTO turmas (nome_turma, id_professor, horario) VALUES 
-- ('Turma A - Manhã', 1, '08:00 - 12:00'),
-- ('Turma B - Tarde', 2, '13:00 - 17:00');

-- Mensagem de sucesso
-- SELECT 'Banco de dados criado com sucesso!' as status;