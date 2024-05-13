use actix_web::{web, App, HttpResponse, HttpServer};
use handlebars::{Handlebars, DirectorySourceOptions};
use sqlx::mysql::MySqlPoolOptions;
use sqlx::migrate::Migrator;
use sqlx::{Pool, MySql};
use actix_files as fs;
use serde_json::json;
use dotenvy::dotenv;
use std::path::Path;
use std::env;

// Os outros programas vem aqui
mod modelos;
mod banco;

async fn indice( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("Indice");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });

    let produtos = match banco::pegar_produtos(&pool).await {Some(p) => p, None => {println!("Erro ao pegar produtos, fazer alguma coisa"); Vec::new()} };
    
    // Renderiza a página
    let body = hb.render("index", &dados).unwrap();

    println!("Indice enviado");
    HttpResponse::Ok().body(body)
}

async fn shop( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("Shop");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("shop", &dados).unwrap();

    println!("Shop enviado");
    HttpResponse::Ok().body(body)
}

async fn blog( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("blog");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("blog", &dados).unwrap();

    println!("Blog enviado");
    HttpResponse::Ok().body(body)
}

async fn about( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("About");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("about", &dados).unwrap();

    println!("About enviado");
    HttpResponse::Ok().body(body)
}

async fn login( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("login");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("login", &dados).unwrap();

    println!("login enviado");
    HttpResponse::Ok().body(body)
}

async fn signin( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("sign in");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("signin", &dados).unwrap();

    println!("signin enviado");
    HttpResponse::Ok().body(body)
}

async fn contact( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("Contato");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("contact", &dados).unwrap();

    println!("Contato enviado");
    HttpResponse::Ok().body(body)
}

async fn cart( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("Cart");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("cart", &dados).unwrap();

    println!("Cart enviado");
    HttpResponse::Ok().body(body)
}

async fn checkout( pool: web::Data<Pool<MySql>>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("Checkout");
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "motd": "Texto vindo do backend"
    });
    
    // Renderiza a página
    let body = hb.render("checkout", &dados).unwrap();

    println!("checkout enviado");
    HttpResponse::Ok().body(body)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Programa iniciado");
    dotenv().expect("Arquivo '.env' não encontrado");
    
    // Cria uma conexão com o banco de dados    
    let url = env::var("URL_BANCO").expect("Endereço do banco não definido");
    let pool = MySqlPoolOptions::new()
    .max_connections(5)
    .connect(url.as_str()).await.expect("Endereço do banco não acessível");

    // Roda as migrações do banco de dados
    println!("Rodando migrações...");
    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .expect("Erro rodando migrações");
    println!("Migrações finalizadas");

    // Cria as configurações que o handlebars irá usar para renderizar
    // as páginas em html com os dados desejados.
    println!("Instânciando HandleBars...");
    let opcoes_hb = DirectorySourceOptions{
        tpl_extension: String::from(".html"), 
        hidden: false, 
        temporary: false};
    let mut hb = Handlebars::new();
    hb.register_templates_directory("./static", opcoes_hb).unwrap();
    let hb_ref = web::Data::new(hb);
    println!("HandleBars instânciado");

    // Instância o servidor http do actix usando as rotas disponíveis;
    println!("Rodando servidor...");
    HttpServer::new(move || {
        App::new()
        .app_data(web::Data::new(pool.clone()))
        .app_data(hb_ref.clone())
        .route("/", web::get().to(indice))
        .route("/shop", web::get().to(shop))
        .route("/blog", web::get().to(blog))
        .route("/about", web::get().to(about))
        .route("/contact", web::get().to(contact))
        .route("/login", web::get().to(login))
        .route("/signin", web::get().to(signin))
        .service(fs::Files::new("/static", "./static"))
    })
    .bind(("0.0.0.0", 9987))?
    .run()
    .await

}