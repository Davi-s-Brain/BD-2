ALTER TABLE Acompanhamento DROP CONSTRAINT IF EXISTS
ID_Acomp_Produ_FK;
alter table Acompanhamento add constraint ID_Acomp_Produ_FK
     foreign key (Indice_prod)
     references Produto;

ALTER TABLE Acompanhamento DROP CONSTRAINT IF EXISTS
REF_Acomp_Estoq_FK;
alter table Acompanhamento add constraint REF_Acomp_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

ALTER TABLE Ambiente DROP CONSTRAINT IF EXISTS
EXCL_Ambiente;
alter table Ambiente add constraint EXCL_Ambiente
     check((Cozinha is TRUE and Salao is FALSE)
           or (Cozinha is FALSE and Salao is TRUE));

ALTER TABLE Avaliacao DROP CONSTRAINT IF EXISTS fk_avaliacao_registra;
