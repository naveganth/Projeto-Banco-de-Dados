use actix_files as fs;
#[allow(unused_imports)]
use actix_web::http::Error;
#[allow(unused_imports)]
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
#[allow(unused_imports)]
use fs::{Files, NamedFile};
use mysql::*;
#[allow(unused_imports)]
use mysql::prelude::*;


async fn indice( pool: web::Data<Pool>, ) -> actix_web::Result<NamedFile> {
    let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
    Ok(NamedFile::open("./paginas/index.html")?)
}


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let url = "mysql://root:senhaboa@localhost:9876/projeti";
    let pool = Pool::new(url).expect("Erro ao conectar ao banco");

    HttpServer::new(move || {
        App::new()
        .app_data(web::Data::new(pool.clone()))
        .route("/", web::get().to(indice))
        .service(fs::Files::new("/estaticos", "./estaticos"))
    })
    .bind(("0.0.0.0", 9000))?
    .run()
    .await
}
