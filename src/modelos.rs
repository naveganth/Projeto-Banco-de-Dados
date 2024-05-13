use std::fmt;
use serde::{Deserialize, Serialize};
use serde_json::Result;


struct Cliente {
    id: u32,
    nome: String,
    sexo: String,
    cpf: String,
    nascimento: String,
    idade: u8,
    ativo: bool,
    email: String,
    senha: String,
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
    pub preco: f32,
    pub estoque: i32,
    pub peso: f32,
    pub cod_barras: String,
    pub desconto: f32,
    pub avaliacao: i8,
    pub url_imagem: String,
}

impl fmt::Display for Produto {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Customize so only `x` and `y` are denoted.
        write!(f, "Produto: (id: {}, nome: {}, preco: {}, estoque: {}, peso: {}, cod_barras: {}, desconto: {}, avaliacao: {}, url_imagem: {})", 
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




