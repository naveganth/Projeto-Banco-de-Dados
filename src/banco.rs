use mysql::*;
use mysql::prelude::*;

pub fn validar_tabelas(pool: &Pool) -> bool{
    let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
    let query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'projeti';";
    let res: std::prelude::v1::Result<Vec<String>, mysql::Error> = conn.exec(query, {});
    if let Ok(resultados) = res {
        if resultados.is_empty() {
            return false
        }
        for resultado in resultados{
            // kkk lembrar como comprara strings aqui
            println!("Resultado: {:?}", resultado);
        }
    }
    false
}

pub fn corrigir_tabelas(pool: &Pool) {
    let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
}