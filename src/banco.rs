#[allow(unused_imports)]
use mysql::*;
#[allow(unused_imports)]
use mysql::prelude::*;

pub fn validar_tabelas(pool: &Pool) -> bool{
    println!("BANCO: Validando tabelas");

    let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
    let query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'projeti';";

    let res: std::prelude::v1::Result<Vec<String>, mysql::Error> = conn.exec(query, {});
    if let Ok(resultados) = res {
        if resultados.is_empty() {
            println!("BANCO: Banco não possui tabela alguma");

            let base = std::fs::read_to_string("./src/sql/base.sql").expect("Falha ao abrir o arquivo base do banco de dados");
            let queries: Vec<&str> = base.split(";")
            .collect();

            for query in queries{
                if query.is_empty(){ continue }

                println!("BANCO: Query de criação da tabela: {}", query);
                conn.query_drop(query).expect("Erro ao criar o banco de dados");
            }
        };
        let tabelas_necessarias = ["Cliente", "Endereco", "Compra", "Produto", "NFE"];

        for tabela in tabelas_necessarias{
            println!("BANCO: Tabela encontrada: {}", &tabela);

            if resultados.contains(&String::from(tabela)) {
                println!("BANCO: Banco contém {}", tabela);
                continue;
            } else {
                return false
            }
        }
    } else {
        println!("BANCO: Não deu pra buscar as tabelas do banco")
    }
    println!("BANCO: Fim da validação de tabelas");
    false
}

pub fn corrigir_tabelas(pool: &Pool) {
    println!("BANCO: Corrigindo tabelas");

    let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
    let query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'projeti';";
    let res: std::prelude::v1::Result<Vec<String>, mysql::Error> = conn.exec(query, {});
    if let Ok(resultados) = res {
        println!("{:?}", resultados);
    }
}