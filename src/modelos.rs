use std::fmt;
use serde::{Deserialize, Serialize};
use serde_json::Result;


#[derive(Deserialize)]
pub struct FormRegistro {
    pub nome: String,
    pub nascimento: String,
    pub sexo: String,
    pub cpf: String,
    pub email: String,
    pub senha: String,
}

impl fmt::Display for FormRegistro {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Produto: (nome: {}, sexo: {}, cpf: {}, nascimento: {}, email: {}, senha: {})", 
                self.nome, self.sexo, self.cpf, self.nascimento, self.email, self.senha)
    }
}

#[derive(Deserialize)]
pub struct Cliente {
    pub id: u32,
    pub nome: String,
    pub sexo: String,
    pub cpf: String,
    pub nascimento: String,
    pub idade: u8,
    pub ativo: bool,
    pub email: String,
    pub senha: String,
}

impl fmt::Display for Cliente {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Produto: (id: {}, nome: {}, sexo: {}, cpf: {}, nascimento: {}, idade: {}, ativo: {}, email: {}, senha: {})", 
                self.id, self.nome, self.sexo, self.cpf, self.nascimento, self.idade, self.ativo, self.email, self.senha)
    }
}

struct Endereco {
    id: u32,
    nome: String,
    logradouro: String,
    cep: String,
    bairro: String,
    cidade: String,
    estado: String,
    pais: String,
    referencia: String,
    numero: String,
    observacao: String,
}

struct Compra {
    id: u32,
    valor_pago: f32,
    forma_pagamento: String,
    data: String,
    endereco: u32,
    cliente: u32,
}

// #[derive(Debug, PartialEq, Eq, Serialize, Deserialize)]
#[derive(sqlx::FromRow, Serialize, Deserialize)]
pub struct Produto {
    pub id: i32,
    pub nome: String,
    pub preco: String,
    pub estoque: i32,
    pub peso: String,
    pub cod_barras: String,
    pub desconto: String,
    pub avaliacao: Vec<i8>,
    pub url_imagem: String,
}

impl fmt::Display for Produto {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Produto: (id: {}, nome: {}, preco: {}, estoque: {}, peso: {}, cod_barras: {}, desconto: {}, avaliacao: {:?}, url_imagem: {})", 
                self.id, self.nome, self.preco, self.estoque, self.peso, self.cod_barras, self.desconto, self.avaliacao, self.url_imagem)
    }
}

struct NFE {
    id: u32,
    servico: String,
    cnpj_empresa: String,
    cod_municipio: String,
    valor_liquido: String,
    pis: f32,
    cofins: f32,
    ir: f32,
    csll: f32,
    iss: f32,
    desconto: f32,
}




