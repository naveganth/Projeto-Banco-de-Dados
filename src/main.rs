use actix_files as fs;
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use fs::{Files, NamedFile};
mod db;

#[get("/")]
async fn indice() -> actix_web::Result<NamedFile> {
    Ok(NamedFile::open("./paginas/index.html")?)
}


#[actix_web::main]
async fn main() -> std::io::Result<()> {

    let db = db::Banco::new("mysql://root:senhaboa@localhost:9876/projeti");
    if let Ok(mut banco) = db {
        println!("Conexão com banco de dados sucedida!");
        println!("Banco: {:?}", banco);

        banco.verificar_tabelas();
        banco.criar_tabelas();
    }

    HttpServer::new(|| {
        App::new()
        .service(indice)
        .service(fs::Files::new("/estaticos", "./estaticos"))
    })
    .bind(("0.0.0.0", 9000))?
    .run()
    .await
}
