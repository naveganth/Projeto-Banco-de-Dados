use std::result;

use sqlx::mysql::MySqlPoolOptions;
use sqlx::{Pool, MySql, Row};
use sqlx::mysql::MySqlRow;
use crate::modelos::{self, *};

pub async fn pegar_produtos(pool: &Pool<MySql>) -> Option<Vec<Produto>>{
    let mut produtos: Vec<Produto> = Vec::new();
    let resultados = sqlx::query("SELECT * FROM Produto").fetch_all(pool).await.expect("Erro");
    
    for resultado in resultados {
        let id: i32 = match resultado.try_get("id") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar id: {}", erro); return None}};
        let nome: &str = match resultado.try_get("nome") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar nome: {}", erro); return None}};
        let estoque: i32 = match resultado.try_get("estoque") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar estoque: {}", erro); return None}};
        let peso: f32 = match resultado.try_get("peso") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar peso: {}", erro); return None}};
        let cod_barras: &str = match resultado.try_get("cod_barras") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar cod_barras: {}", erro); return None}};
        let desconto: f32 = match resultado.try_get("desconto") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar desconto: {}", erro); return None}};
        let preco: f32 = match resultado.try_get("preco") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar preco: {}", erro); return None}};
        let avaliacao: Vec<i8> = match resultado.try_get("avaliacao") {Ok(id) => (0..id).collect(), Err(erro) => {println!("Erro ao pegar avaliacao: {}", erro); return None}};
        let url_imagem: &str = match resultado.try_get("url_imagem") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar url_imagem: {}", erro); return None}};
        
        let string_peso = format!("{:.2}", peso);
        let string_desconto = format!("{:.2}", desconto);
        let string_preco = format!("{:.2}", preco);

        let produto = Produto{ id: id, nome: String::from(nome), estoque: estoque, peso: string_peso, 
                                        cod_barras: String::from(cod_barras), desconto: string_desconto, 
                                        avaliacao: avaliacao, url_imagem: String::from(url_imagem), preco: string_preco};

        println!("Produto encontrado: {}", produto);
        produtos.push(produto);
    }

    Some(produtos)
}

pub async fn pegar_produtos_populares(pool: &Pool<MySql>) -> Option<Vec<Produto>>{
    let mut produtos: Vec<Produto> = Vec::new();
    let resultados = sqlx::query("SELECT * FROM Produto limit 4").fetch_all(pool).await.expect("Erro");

    for resultado in resultados {
        let id: i32 = match resultado.try_get("id") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar id: {}", erro); return None}};
        let nome: &str = match resultado.try_get("nome") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar nome: {}", erro); return None}};
        let estoque: i32 = match resultado.try_get("estoque") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar estoque: {}", erro); return None}};
        let peso: f32 = match resultado.try_get("peso") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar peso: {}", erro); return None}};
        let cod_barras: &str = match resultado.try_get("cod_barras") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar cod_barras: {}", erro); return None}};
        let desconto: f32 = match resultado.try_get("desconto") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar desconto: {}", erro); return None}};
        let preco: f32 = match resultado.try_get("preco") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar preco: {}", erro); return None}};
        let avaliacao: Vec<i8> = match resultado.try_get("avaliacao") {Ok(id) => (0..id).collect(), Err(erro) => {println!("Erro ao pegar avaliacao: {}", erro); return None}};
        let url_imagem: &str = match resultado.try_get("url_imagem") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar url_imagem: {}", erro); return None}};
        
        let string_peso = format!("{:.2}", peso);
        let string_desconto = format!("{:.2}", desconto);
        let string_preco = format!("{:.2}", preco);

        let produto = Produto{ id: id, nome: String::from(nome), estoque: estoque, peso: string_peso, 
                                        cod_barras: String::from(cod_barras), desconto: string_desconto, 
                                        avaliacao: avaliacao, url_imagem: String::from(url_imagem), preco: string_preco};

        println!("Produto encontrado: {}", produto);
        produtos.push(produto);
    }

    Some(produtos)
}

pub async fn criar_cliente(pool: &Pool<MySql>, registro: modelos::FormRegistro) {
    // let nome = registro.nome;
    // let sexo = registro.sexo;
    // let cpf = registro.cpf;
    // let nascimento = registro.nascimento;
    // let idade: = registro.nascimento;
    // let ativo = true;
    // let email = registro.email;
    // let senha = registro.senha;
}