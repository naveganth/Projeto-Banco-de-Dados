struct Cliente {
    id: u32,
    nome: String,
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
    logradouto: String,
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

struct Produto {
    id: u32,
    nome: String,
    estoque: u32,
    peso: u32,
    cod_barras: String,
    desconto: f32
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




