
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
pub struct Produto {
    pub id: i32,
    pub nome: String,
    pub preco: String,
    pub estoque: i32,
    pub peso: String,
    pub cod_barras: String,
    pub desconto: String,
    pub avaliacao: i8,
    pub url_imagem: String,
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




