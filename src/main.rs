use actix_files as fs;
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use fs::{Files, NamedFile};

#[get("/")]
async fn indice() -> actix_web::Result<NamedFile> {
    Ok(NamedFile::open("./paginas/index.html")?)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
        .service(indice)
        .service(fs::Files::new("/estaticos", "./estaticos"))
    })
    .bind(("0.0.0.0", 9000))?
    .run()
    .await
}
