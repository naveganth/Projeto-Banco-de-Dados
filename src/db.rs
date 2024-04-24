use mysql::*;
use mysql::prelude::*;

#[derive(Debug)]
pub struct Banco{
    conn: Option<PooledConn>,
}

impl Banco {
    pub fn new(url: &str) -> Result<Banco> {

        // let url = "mysql://root:password@localhost:3307/db_name";
        // let pool = Pool::new(url)?;

        let pool = Pool::new(url)?;
        let mut conn = pool.get_conn()?;

        Ok(Banco{conn: Some(conn)})
    }

    pub fn verificar_tabelas(&mut self) {
        println!("Banco: Verificando tabelas");
    }

    pub fn criar_tabelas(&mut self) {
        println!("Banco: criando tabelas");
    }
}