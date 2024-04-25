use actix_files as fs;
use actix_web::http::Error;
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use fs::{Files, NamedFile};
use mysql::*;
use mysql::prelude::*;
use serde_json::json;
use handlebars::{Handlebars, DirectorySourceOptions};

mod modelos;
mod banco;


async fn indice( pool: web::Data<Pool>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("Indice");
    let mut conn = pool.get_conn().expect("Erro ao conectar ao banco de dados");
    
    let dados = json!({
        "teste": "adhdfhjdshkesfhdksbaba"
    });

    println!("Dados: {}", dados);
    let body = hb.render("index", &dados).unwrap();
    HttpResponse::Ok().body(body)
}


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let url = "mysql://root:senhaboa@localhost:9876/projeti";
    let pool = Pool::new(url).expect("Erro ao conectar ao banco");

    // Se as tabelas do banco não estiverem certas, corrige elas
    if !banco::validar_tabelas(&pool) {
        banco::corrigir_tabelas(&pool);
    }

    let opcoes_hb = handlebars::DirectorySourceOptions{tpl_extension: String::from(".html"), hidden: false, temporary: false};
    let mut hb = Handlebars::new();
    hb.register_templates_directory("./paginas", opcoes_hb).unwrap();
    let hb_ref = web::Data::new(hb);

    HttpServer::new(move || {
        App::new()
        .app_data(web::Data::new(pool.clone()))
        .app_data(hb_ref.clone())
        .route("/", web::get().to(indice))
        .service(fs::Files::new("/estaticos", "./estaticos"))
    })
    .bind(("0.0.0.0", 9000))?
    .run()
    .await
}
