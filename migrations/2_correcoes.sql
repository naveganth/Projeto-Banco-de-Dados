ALTER TABLE Produto 
ADD preco decimal(5, 2);

ALTER TABLE Produto 
MODIFY desconto decimal(5, 2);

ALTER TABLE Produto 
ADD avaliacao int;

ALTER TABLE Produto 
ADD url_imagem varchar(255);