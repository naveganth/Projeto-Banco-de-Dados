CREATE TABLE Cliente(
    id int PRIMARY KEY AUTO_INCREMENT,
    nome varchar(255) not null,
    cpf varchar(255) not null,
    nascimento date not null,
    idade int(3) not null,
    ativo boolean not null,
    email varchar(255) not null,
    senha varchar(255) not null
);

CREATE TABLE Endereco(
    id int PRIMARY KEY AUTO_INCREMENT,
    nome varchar(255) not null,
    logradouro varchar(255) not null,
    cep varchar(255) not null,
    bairro varchar(255) not null,
    cidade varchar(255) not null,
    estado varchar(255) not null,
    pais varchar(255) not null,
    referencia varchar(255) not null,
    numero int not null,
    observacao varchar(255) not null,
    cliente int not null,
    FOREIGN KEY (cliente) REFERENCES Cliente(id)
);

CREATE TABLE Compra(
    id int PRIMARY KEY AUTO_INCREMENT,
    valor_pago decimal(11, 2) not null,
    forma_pagamento varchar(255) not null,
    data date not null,
    endereco int not null,
    cliente int not null,
    FOREIGN KEY (endereco) REFERENCES Endereco(id),
    FOREIGN KEY (cliente) REFERENCES Cliente(id)
);

CREATE TABLE Produto(
    id int PRIMARY KEY AUTO_INCREMENT,
    nome varchar(255) not null,
    estoque int not null,
    peso decimal(11, 2) not null,
    cod_barras varchar(255) not null,
    desconto decimal(3, 2) not null
);

CREATE TABLE CompraProduto(
    id int PRIMARY KEY AUTO_INCREMENT,
    compra int not null,
    produto int not null,
    FOREIGN KEY (compra) REFERENCES Compra(id),
    FOREIGN KEY (produto) REFERENCES Produto(id)
);

CREATE TABLE NFE(
    id int PRIMARY KEY AUTO_INCREMENT,
    servico varchar(255) NOT null,
    cnpj_empresa varchar(255) NOT null,
    cod_municipio varchar(255) NOT NULL,
    valor_liquido decimal(11, 2) NOT NULL,
    pis decimal(11, 2) NOT NULL,
    cofins decimal(11, 2) NOT NULL,
    ir decimal(11, 2) NOT NULL,
    csll decimal(11, 2) NOT NULL,
    iss decimal(11, 2) NOT NULL,
    desconto decimal (3, 2) NOT NULL,
    compra int,
    FOREIGN KEY (compra) REFERENCES Compra(id)
);