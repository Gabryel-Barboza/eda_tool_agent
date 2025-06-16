USE n8n_notas_fiscais;

DROP TABLE IF EXISTS itens_notas_fiscais , notas_fiscais;

CREATE TABLE IF NOT EXISTS notas_fiscais(
    chave_acesso VARCHAR(44) PRIMARY KEY NOT NULL,
    modelo VARCHAR(70) NOT NULL,
    serie VARCHAR(3) NOT NULL,
    numero VARCHAR(9) NOT NULL,
    natureza_operacao VARCHAR(60) NOT NULL,
    data_emissao DATETIME NOT NULL,
    evento_mais_recente VARCHAR(255),
    data_hora_evento_mais_recente DATETIME,
    cnpj_cpf_emitente VARCHAR(14) NOT NULL,
    razao_social_emitente VARCHAR(255) NOT NULL,
    inscricao_estadual_emitente VARCHAR(14),
    uf_emitente CHAR(2) NOT NULL,
    municipio_emitente VARCHAR(100),
    cnpj_destinatario VARCHAR(14),
    nome_destinatario VARCHAR(255),
    uf_destinatario CHAR(2),
    indicador_ie_destinatario ENUM("NÃO CONTRIBUINTE", "CONTRIBUINTE ISENTO", "CONTRIBUINTE ICMS"),
    destino_operacao VARCHAR(100) NOT NULL,
    consumidor_final VARCHAR(100) NOT NULL,
    presenca_comprador VARCHAR(100) NOT NULL,
    valor_nota_fiscal DECIMAL(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS itens_notas_fiscais(
    id INT PRIMARY KEY AUTO_INCREMENT,
    chave_acesso_nf VARCHAR(44) NOT NULL,
    numero_produto INT NOT NULL,
    descricao_produto_servico VARCHAR(500) NOT NULL,
    codigo_ncm_sh VARCHAR(8),
    ncm_sh_tipo_produto VARCHAR(255),
    cfop VARCHAR(4) NOT NULL,
    quantidade DECIMAL(15, 4) NOT NULL,
    unidade VARCHAR(6) NOT NULL,
    valor_unitario DECIMAL(15, 2) NOT NULL,
    valor_total DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (chave_acesso_nf) REFERENCES notas_fiscais(chave_acesso)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
