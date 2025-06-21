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

ALTER TABLE Bebida DROP CONSTRAINT IF EXISTS ID_Bebid_Produ_FK;
alter table Bebida add constraint ID_Bebid_Produ_FK
     foreign key (Indice_prod)
     references Produto;

ALTER TABLE Bebida DROP CONSTRAINT IF EXISTS REF_Bebid_Estoq_FK;
alter table Bebida add constraint REF_Bebid_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

ALTER TABLE Brinde DROP CONSTRAINT IF EXISTS SID_Brind_Lanch_FK;
alter table Brinde add constraint SID_Brind_Lanch_FK
     foreign key (Indice_prod)
     references Lanche;

ALTER TABLE Brinde DROP CONSTRAINT IF EXISTS REF_Brind_Estoq_FK;
alter table Brinde add constraint REF_Brind_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

ALTER TABLE Ped_Escolhe_Prod DROP CONSTRAINT IF EXISTS REF_C_Esc_Produ;
alter table Ped_Escolhe_Prod add constraint REF_C_Esc_Produ
     foreign key (Indice_prod)
     references Produto;

ALTER TABLE C_Registra_A DROP CONSTRAINT IF EXISTS ID_C_Reg_Pedid_FK;
alter table C_Registra_A add constraint ID_C_Reg_Pedid_FK
     foreign key (Id_pedido)
     references Pedido;

ALTER TABLE C_Registra_A DROP CONSTRAINT IF EXISTS SID_C_Reg_Clien_FK;
alter table C_Registra_A add constraint SID_C_Reg_Clien_FK
     foreign key (Id_cliente)
     references Cliente;

ALTER TABLE C_Registra_A DROP CONSTRAINT IF EXISTS SID_C_Reg_Avali_FK;
alter table C_Registra_A add constraint SID_C_Reg_Avali_FK
     foreign key (Indice_av)
     references Avaliacao;

ALTER TABLE Cozinha DROP CONSTRAINT IF EXISTS ID_Cozin_Ambie_FK;
alter table Cozinha add constraint ID_Cozin_Ambie_FK
     foreign key (Id_Amb)
     references Ambiente;

ALTER TABLE F_Vende_P DROP CONSTRAINT IF EXISTS EQU_F_Ven_Produ;
alter table F_Vende_P add constraint EQU_F_Ven_Produ
     foreign key (Indice_prod)
     references Produto;

ALTER TABLE F_Vende_P DROP CONSTRAINT IF EXISTS EQU_F_Ven_Franq_FK;
alter table F_Vende_P add constraint EQU_F_Ven_Franq_FK
     foreign key (Id_franquia)
     references Franquia;

ALTER TABLE Ingrediente DROP CONSTRAINT IF EXISTS REF_Ingre_Estoq_FK;
alter table Ingrediente add constraint REF_Ingre_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

ALTER TABLE L_Contem_I DROP CONSTRAINT IF EXISTS EQU_L_Con_Lanch_FK;
alter table L_Contem_I add constraint EQU_L_Con_Lanch_FK
     foreign key (Indice_prod)
     references Lanche;

ALTER TABLE L_Contem_I DROP CONSTRAINT IF EXISTS REF_L_Con_Ingre;
alter table L_Contem_I add constraint REF_L_Con_Ingre
     foreign key (Id_ingred)
     references Ingrediente;

ALTER TABLE Lanche DROP CONSTRAINT IF EXISTS ID_Lanch_Produ_FK;
alter table Lanche add constraint ID_Lanch_Produ_FK
     foreign key (Indice_prod)
     references Produto;

ALTER TABLE Pedido DROP CONSTRAINT IF EXISTS REF_Pedid_Funci_FK;
alter table Pedido add constraint REF_Pedid_Funci_FK
     foreign key (Id_func)
     references Funcionario;

ALTER TABLE Pedido DROP CONSTRAINT IF EXISTS EQU_Pedid_Clien_FK;
alter table Pedido add constraint EQU_Pedid_Clien_FK
     foreign key (Id_cliente)
     references Cliente;

ALTER TABLE Salao DROP CONSTRAINT IF EXISTS ID_Salao_Ambie_FK;
alter table Salao add constraint ID_Salao_Ambie_FK
     foreign key (Id_Amb)
     references Ambiente;

ALTER TABLE Sobremesa DROP CONSTRAINT IF EXISTS REF_Sobre_Estoq_FK;
alter table Sobremesa add constraint REF_Sobre_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

ALTER TABLE Sobremesa DROP CONSTRAINT IF EXISTS ID_Sobre_Produ_FK;
alter table Sobremesa add constraint ID_Sobre_Produ_FK
     foreign key (Indice_prod)
     references Produto;

ALTER TABLE Produto DROP CONSTRAINT IF EXISTS EXCL_Produto;
alter table Produto add constraint EXCL_Produto
     check((Acompanhamento is TRUE and Sobremesa is FALSE and Lanche is FALSE and Bebida is FALSE)
           or (Acompanhamento is FALSE and Sobremesa is TRUE and Lanche is FALSE and Bebida is FALSE)
           or (Acompanhamento is FALSE and Sobremesa is FALSE and Lanche is TRUE and Bebida is FALSE)
           or (Acompanhamento is FALSE and Sobremesa is FALSE and Lanche is FALSE and Bebida is TRUE)
           or (Acompanhamento is FALSE and Sobremesa is FALSE and Lanche is FALSE and Bebida is FALSE));

--