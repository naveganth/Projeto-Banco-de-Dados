use actix_files as fs;
use actix_web::{web, App, HttpResponse, HttpServer};
use mysql::*;
use serde_json::json;
use handlebars::{Handlebars, DirectorySourceOptions};

// Os outros programas vem aqui
mod modelos;
mod banco;


async fn indice( pool: web::Data<Pool>, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    println!("Indice");
    // Envia uma referência do pool para fazer uma consulta no banco
    banco::validar_tabelas(&pool);
    
    // Imagina que aqui tem dados que foram recebidos do banco
    let dados = json!({
        "teste": "adhdfhjdshkesfhdksbaba"
    });

    // Renderiza a página
    let body = hb.render("index", &dados).unwrap();

    println!("Indice enviado com sucesso!");
    HttpResponse::Ok().body(body)
}


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // substituir isso aqui por variáveis de ambiente do docker;
    let url = "mysql://root:senhaboa@localhost:9876/projeti";
    let pool = Pool::new(url).expect("Erro ao conectar ao banco");

    // Se as tabelas do banco não estiverem certas, corrige elas
    if !banco::validar_tabelas(&pool) {
        banco::corrigir_tabelas(&pool);
    }

    // Cria as configurações que o handlebars irá usar para renderizar
    // as páginas em html com os dados desejados.
    let opcoes_hb = DirectorySourceOptions{
        tpl_extension: String::from(".html"), 
        hidden: false, 
        temporary: false};
    let mut hb = Handlebars::new();
    hb.register_templates_directory("./static", opcoes_hb).unwrap();
    let hb_ref = web::Data::new(hb);

    // Instância o servidor http do actix usando as rotas disponíveis;
    HttpServer::new(move || {
        App::new()
        .app_data(web::Data::new(pool.clone()))
        .app_data(hb_ref.clone())
        .route("/", web::get().to(indice))
        .service(fs::Files::new("/static", "./static"))
    })
    .bind(("0.0.0.0", 9000))?
    .run()
    .await

}
