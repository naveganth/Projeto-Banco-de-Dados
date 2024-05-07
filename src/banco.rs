use sqlx::mysql::MySqlPoolOptions;
use sqlx::{Pool, MySql};
use sqlx::mysql::MySqlRow;
use crate::modelos::*;

pub async fn validar_tabelas(pool: &Pool<MySql>) -> bool{
    println!("BANCO: Validando tabelas");

    let resultados: Vec<sqlx::mysql::MySqlRow> = sqlx::query(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'projeti'")
        .fetch_all(pool).await.expect("Erro ao executar query");

    for resultado in resultados{
        println!("Resultado: {:?}", resultado);
    }
    // let res: std::prelude::v1::Result<Vec<String>, mysql::Error> = conn.exec(query, {});
    // if let Ok(resultados) = res {
    //     if resultados.is_empty() {
    //         println!("BANCO: Banco não possui tabela alguma");

    //         let base = std::fs::read_to_string("./src/sql/base.sql").expect("Falha ao abrir o arquivo base do banco de dados");
    //         let queries: Vec<&str> = base.split(";")
    //         .collect();

    //         for query in queries{
    //             if query.is_empty(){ continue }

    //             println!("BANCO: Query de criação da tabela: {}", query);
    //             conn.query_drop(query).expect("Erro ao criar o banco de dados");
    //         }
    //     };
    //     let tabelas_necessarias = ["Cliente", "Endereco", "Compra", "Produto", "NFE"];

    //     for tabela in tabelas_necessarias{
    //         println!("BANCO: Tabela encontrada: {}", &tabela);

    //         if resultados.contains(&String::from(tabela)) {
    //             println!("BANCO: Banco contém {}", tabela);
    //             continue;
    //         } else {
    //             return false
    //         }
    //     }
    //     return true

    // } else {
    //     println!("BANCO: Não deu pra buscar as tabelas do banco")
    // }
    // println!("BANCO: Fim da validação de tabelas");
    false
}

pub fn corrigir_tabelas(pool: &Pool<MySql>) {
    // println!("BANCO: Corrigindo tabelas");

    // let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
    // let query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'projeti';";
    // let res: std::prelude::v1::Result<Vec<String>, mysql::Error> = conn.exec(query, {});
    // if let Ok(resultados) = res {
    //     println!("{:?}", resultados);
    // }
}

pub fn pegar_produtos(pool: &Pool<MySql>){  //  -> Vec<Produto>
    // let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
    // let query = "SELECT id, nome, preco, estoque, peso, cod_barras, desconto, avaliacao, url_imagem FROM Produto LIMIT 4";

    // let produtos: std::prelude::v1::Result<Vec<Produto>, Error> = conn.query_map(query, 
    //     |(id, nome, preco, estoque, peso, cod_barras, desconto, avaliacao, url_imagem)| {
    //         Produto{id, nome, preco, estoque, peso, cod_barras, desconto, avaliacao, url_imagem}
    //     });

    // match produtos{
    //     Ok(produtos) => { return produtos},
    //     Err(erro) => { 
    //         println!("Erro ao buscar produtos");
    //         vec![]
    //     },
    // }
}

pub fn pegar_produtos_populares(pool: &Pool<MySql>) {
    
}