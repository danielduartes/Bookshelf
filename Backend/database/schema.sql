PRAGMA foreign_keys = ON;

-- Usuários
CREATE TABLE IF NOT EXISTS usuario (
  id              INTEGER PRIMARY KEY,
  nome            TEXT NOT NULL,
  email           TEXT NOT NULL UNIQUE,
  filme_favorito  TEXT,
  criado_em       TEXT NOT NULL DEFAULT (datetime('now'))
) STRICT;

-- Livros
CREATE TABLE IF NOT EXISTS livro (
  id                  INTEGER PRIMARY KEY,
  nome                TEXT NOT NULL,
  descricao           TEXT,
  data_publicacao     TEXT,                          -- YYYY-MM-DD
  classificacao_indicativa TEXT NOT NULL
    CHECK (classificacao_indicativa IN ('L','10','12','14','16','18')),
  url_imagem          TEXT,
  public_domain       INTEGER NOT NULL DEFAULT 0     -- 0 = não, 1 = sim
    CHECK (public_domain IN (0,1)),
  criado_em           TEXT NOT NULL DEFAULT (datetime('now'))
) STRICT;

-- Gêneros
CREATE TABLE IF NOT EXISTS genero (
  id              INTEGER PRIMARY KEY,
  genero          TEXT NOT NULL UNIQUE
) STRICT;

-- N:N Livro-Gênero
CREATE TABLE IF NOT EXISTS livro_genero (
  id              INTEGER PRIMARY KEY,
  livro_id        INTEGER NOT NULL REFERENCES livro(id) ON DELETE CASCADE,
  genero_id       INTEGER NOT NULL REFERENCES genero(id) ON DELETE RESTRICT,
  UNIQUE (livro_id, genero_id)
) STRICT;

-- Preferências de gêneros do usuário
CREATE TABLE IF NOT EXISTS user_preferencias (
  id              INTEGER PRIMARY KEY,
  usuario_id      INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
  genero_id       INTEGER NOT NULL REFERENCES genero(id) ON DELETE RESTRICT,
  UNIQUE (usuario_id, genero_id)
) STRICT;

-- Notas
CREATE TABLE IF NOT EXISTS notas (
  id              INTEGER PRIMARY KEY,
  usuario_id      INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
  livro_id        INTEGER NOT NULL REFERENCES livro(id) ON DELETE CASCADE,
  nota            REAL NOT NULL CHECK (nota >= 0 AND nota <= 5),
  descricao       TEXT,
  criado_em       TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (usuario_id, livro_id)
) STRICT;

-- Registro (um livro adicionado pelo usuário)
CREATE TABLE IF NOT EXISTS registro (
  id              INTEGER PRIMARY KEY,
  usuario_id      INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
  livro_id        INTEGER NOT NULL REFERENCES livro(id) ON DELETE CASCADE,
  total_paginas   INTEGER NOT NULL CHECK (total_paginas > 0),
  criado_em       TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (usuario_id, livro_id)
) STRICT;

-- Registros (logs de progresso)
CREATE TABLE IF NOT EXISTS registros (
  id              INTEGER PRIMARY KEY,
  registro_id     INTEGER NOT NULL REFERENCES registro(id) ON DELETE CASCADE,
  pagina_atual    INTEGER NOT NULL CHECK (pagina_atual >= 0),
  data_registro   TEXT NOT NULL DEFAULT (datetime('now'))
) STRICT;

-- Tags
CREATE TABLE IF NOT EXISTS tags (
  id              INTEGER PRIMARY KEY,
  tag             TEXT NOT NULL UNIQUE
    CHECK (length(trim(tag)) > 0)
) STRICT;

-- Associação de tags a (usuario, livro)
CREATE TABLE IF NOT EXISTS tag_usuario_livro (
  id              INTEGER PRIMARY KEY,
  usuario_id      INTEGER NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
  livro_id        INTEGER NOT NULL REFERENCES livro(id) ON DELETE CASCADE,
  tag_id          INTEGER NOT NULL REFERENCES tags(id) ON DELETE RESTRICT,
  criado_em       TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (usuario_id, livro_id, tag_id)
) STRICT;

-- Índices úteis
CREATE INDEX IF NOT EXISTS idx_livro_nome ON livro(nome);
CREATE INDEX IF NOT EXISTS idx_livro_genero_genero ON livro_genero(genero_id);
CREATE INDEX IF NOT EXISTS idx_pref_usuario ON user_preferencias(usuario_id);
CREATE INDEX IF NOT EXISTS idx_notas_livro ON notas(livro_id);
CREATE INDEX IF NOT EXISTS idx_registro_usuario ON registro(usuario_id);
CREATE INDEX IF NOT EXISTS idx_registros_registro ON registros(registro_id);
CREATE INDEX IF NOT EXISTS idx_tul_usuario_livro ON tag_usuario_livro(usuario_id, livro_id);

-- Seeds: tags padrão
INSERT INTO tags (tag) VALUES 
  ('Lendo'),
  ('Abandonado'),
  ('Quero ler')
ON CONFLICT(tag) DO NOTHING;

-- Seeds: gêneros básicos
INSERT INTO genero (genero) VALUES
  ('Ficção'),
  ('Fantasia'),
  ('Romance'),
  ('Terror'),
  ('Suspense'),
  ('Aventura'),
  ('História'),
  ('Ciência'),
  ('Biografia'),
  ('Autoajuda')
ON CONFLICT(genero) DO NOTHING;
