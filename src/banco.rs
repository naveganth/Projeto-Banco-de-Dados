use std::result;

use sqlx::mysql::MySqlPoolOptions;
use sqlx::{Pool, MySql, Row};
use sqlx::mysql::MySqlRow;
use crate::modelos::*;

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
        let avaliacao: i8 = match resultado.try_get("avaliacao") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar avaliacao: {}", erro); return None}};
        let url_imagem: &str = match resultado.try_get("url_imagem") {Ok(id) => id, Err(erro) => {println!("Erro ao pegar url_imagem: {}", erro); return None}};

        let produto = Produto{ id: id, nome: String::from(nome), estoque: estoque, peso: peso, 
                                        cod_barras: String::from(cod_barras), desconto: desconto, 
                                        avaliacao: avaliacao, url_imagem: String::from(url_imagem), preco: preco};

        println!("Produto encontrado: {}", produto);
        produtos.push(produto);
    }

    Some(produtos)
}

pub fn pegar_produtos_populares(pool: &Pool<MySql>) {
    
}