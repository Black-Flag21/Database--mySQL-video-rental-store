CREATE TABLE clienti (
    id_client             NUMBER(4) NOT NULL,
    serie_act_identitate  VARCHAR2(20) NOT NULL,
    tip_act               VARCHAR2(15) NOT NULL,
    nume                  VARCHAR2(20) NOT NULL,
    prenume               VARCHAR2(20) NOT NULL,
    email                 VARCHAR2(50),
    nr_telefon            CHAR(10) NOT NULL,
    data_nasterii         DATE NOT NULL
)
LOGGING;



ALTER TABLE clienti
    ADD CONSTRAINT clienti_serie_act_ck CHECK ( REGEXP_LIKE ( serie_act_identitate,
                                                              '^[A-Z0-9 ]*$' ) );

ALTER TABLE clienti
    ADD CONSTRAINT clienti_ti_act_ck CHECK ( tip_act IN ( 'Altele', 'CI', 'Pasaport' ) );

ALTER TABLE clienti
    ADD CONSTRAINT clienti_nume_ck CHECK ( length(nume) >= 2 AND REGEXP_LIKE ( nume,'^[a-zA-Z ]*$' ) );

ALTER TABLE clienti
    ADD CONSTRAINT clienti_prenume_ck CHECK ( length(prenume) >= 2 AND REGEXP_LIKE ( prenume,'^[a-zA-Z ]*$' ) );

ALTER TABLE clienti
    ADD CONSTRAINT clienti_email_ck CHECK ( REGEXP_LIKE ( email,'[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}' ) );

ALTER TABLE clienti
    ADD CONSTRAINT clienti_nr_telefon_ck CHECK ( length(nr_telefon) = 10
        AND REGEXP_LIKE ( nr_telefon, '^[0][:7:3:2][0-9 ]*$' ) );


ALTER TABLE clienti ADD CONSTRAINT clienti_pk PRIMARY KEY ( id_client );
alter table clienti drop constraint clienti_pk;



ALTER TABLE clienti ADD CONSTRAINT clienti_nr_telefon_uk UNIQUE ( nr_telefon );

ALTER TABLE clienti ADD CONSTRAINT clienti_email_uk UNIQUE ( email );


CREATE TABLE contracte_inchirieri (
    nr_contract      NUMBER(4) NOT NULL,
    data_inchiriere  DATE NOT NULL,
    data_retur       DATE NOT NULL,
    tarif            NUMBER(4) NOT NULL,
    id_client        NUMBER(4) NOT NULL,
    id_film          NUMBER(4) NOT NULL
)
LOGGING;

ALTER TABLE contracte_inchirieri
    ADD CONSTRAINT contracte_data_inchiriere_ck CHECK ( to_char(data_inchiriere, 'YYYY-MM-DD') >= '2020-01-01' );

ALTER TABLE contracte_inchirieri
    ADD CONSTRAINT contracte_data_retur_ck CHECK ( data_retur > data_inchiriere AND data_retur < add_months(data_inchiriere, 1) );

ALTER TABLE contracte_inchirieri ADD CONSTRAINT contracte_inchirieri_pk PRIMARY KEY ( nr_contract,id_film );
                                                                                      
ALTER TABLE contracte_inchirieri ADD CONSTRAINT contracte_inchirieri_tarif_ck CHECK ( tarif > 10 );


CREATE TABLE detalii_film (
    id_film                 NUMBER(4) NOT NULL,
    nume                    VARCHAR2(20) NOT NULL,
    gen_film                VARCHAR2(20) NOT NULL,
    durata_min              NUMBER(4) NOT NULL,
    an_aparitie             NUMBER(4) NOT NULL,
    actor_principal         VARCHAR2(25) NOT NULL,
    tip_film                VARCHAR2(10) NOT NULL,
    restrictie_varsta       NUMBER(2) NOT NULL,
    tarif                   NUMBER(3) NOT NULL
)
LOGGING;

ALTER TABLE detalii_film
    ADD CONSTRAINT detalii_film_nume_ck CHECK ( length(nume) >= 2 AND REGEXP_LIKE ( nume,'^[a-zA-Z ]*$' ) );
                                                                     
ALTER TABLE detalii_film   
    ADD CONSTRAINT detalii_film_gen_film_ck CHECK ( length(gen_film) >= 2 AND REGEXP_LIKE ( gen_film, '^[a-zA-Z ]*$' ) );

ALTER TABLE detalii_film
    ADD CONSTRAINT detalii_an_aparitie_ck CHECK ( an_aparitie BETWEEN 1980 AND 2023 );
    
ALTER TABLE detalii_film
    ADD CONSTRAINT detalii_film_tip_film_ck CHECK ( tip_film IN ( '2D', '3D' ) );
    
ALTER TABLE detalii_film
    ADD CONSTRAINT detalii_film_actor_principal_ck CHECK ( length(actor_principal) >= 2 AND REGEXP_LIKE ( actor_principal, '^[a-zA-Z ]*$' ) );

ALTER TABLE detalii_film
    ADD CONSTRAINT detalii_film_restrictie_varsta_ck CHECK (  restrictie_varsta  IN ( 12, 15,18 ) );

ALTER TABLE detalii_film
    ADD CONSTRAINT detalii_film_durata_min_ck CHECK ( durata_min BETWEEN 1 AND 300 );
    
ALTER TABLE detalii_film ADD CONSTRAINT detalii_film_tarif_ck CHECK ( tarif > 10 );
                                                                
ALTER TABLE detalii_film ADD CONSTRAINT detalii_film_pk PRIMARY KEY (id_film);            


CREATE TABLE particularitati (
    id_particularitati              NUMBER(2) NOT NULL,
    Box_office                      NUMBER(11) NOT NULL,
    nume_regizor                    VARCHAR2(30) NOT NULL,
    companie_producatoare           VARCHAR2(30) NOT NULL
)
LOGGING;


ALTER TABLE particularitati
    ADD CONSTRAINT particularitati_nume_regizor_ck CHECK ( length(nume_regizor) >= 2
        AND REGEXP_LIKE ( nume_regizor, '^[a-zA-Z ]*$' ) );

ALTER TABLE particularitati
    ADD CONSTRAINT particularitati_companie_producatoare_ck CHECK ( length(companie_producatoare) >= 2
        AND REGEXP_LIKE ( companie_producatoare, '^[a-zA-Z ]*$' ) );

ALTER TABLE particularitati ADD CONSTRAINT particularitati_Box_office_ck CHECK ( Box_office > 1000000 );

ALTER TABLE particularitati ADD CONSTRAINT particularitati_pk PRIMARY KEY ( id_particularitati );
      

CREATE TABLE film (
    id_film         NUMBER(4) NOT NULL,
    buget           NUMBER(10) NOT NULL
)
LOGGING;      

ALTER TABLE film ADD CONSTRAINT film_buget_ck CHECK ( buget > 500000 );

ALTER TABLE film ADD CONSTRAINT film_pk PRIMARY KEY ( id_film );

                
CREATE TABLE film_particularitati (
    id_film             NUMBER(4) NOT NULL,
    id_particularitati  NUMBER(2) NOT NULL
)
LOGGING;     


ALTER TABLE film_particularitati ADD CONSTRAINT film_particularitati_pk PRIMARY KEY (id_particularitati,id_film);

ALTER TABLE contracte_inchirieri
    ADD CONSTRAINT clienti_contracte_fk FOREIGN KEY ( id_client ) REFERENCES clienti ( id_client );
    
   
ALTER TABLE contracte_inchirieri
    ADD CONSTRAINT film_contracte_inchirieri_fk FOREIGN KEY ( id_film ) REFERENCES film ( id_film );
            
ALTER TABLE detalii_film
    ADD CONSTRAINT film_detalii_film FOREIGN KEY ( id_film )
        REFERENCES film ( id_film );
  
ALTER TABLE film_particularitati
    ADD CONSTRAINT film_particularitati_particularitati_fk FOREIGN KEY ( id_particularitati )
        REFERENCES particularitati ( id_particularitati );
            
ALTER TABLE film_particularitati
    ADD CONSTRAINT film_particularitati_film_fk FOREIGN KEY ( id_film ) REFERENCES film ( id_film ) ;


insert into CLIENTI values (1,'VS','CI','Salavastru','Andrei','andrei-ionut.salavastru@student.tuiasi.ro','0761609550','14-JAN-2001');
insert into CLIENTI values (2,'IS','CI','Teslaru','Victor','victor.teslaru@student.tuiasi.ro','0746540091','23-JUN-2001');
insert into CLIENTI values (3,'XS','CI','Luchian','Alexandru','alexandru.luchian@student.tuiasi.ro','0756727899','16-FEB-2001');
insert into CLIENTI values (4,'LM','Pasaport','Paduraru','George','george.paduraru@student.tuiasi.ro','0751919164','23-OCT-2001');
insert into CLIENTI values (5,'IS','Pasaport','Ivanov','Ioan','ioan.ivanov@student.tuiasi.ro','0764008240','21-MAY-2004');



insert into film values(1,237000000);
insert into film values(2,38000000);
insert into film values(3,78000000);
insert into film values(4,30000000);
insert into film values(5,200000000);
insert into film values(6,63000000);
insert into film values(7,18000000);
insert into film values(8,60000000);
insert into film values(9,40000000);
insert into film values(10,22000000);

insert into detalii_film values(1,'Avatar','SF',162,2009,'Sam Worthington','3D',12,24);
insert into detalii_film values(2,'Fast and Furoius','Thriller',106,2001,'Vin Diesel','2D',12,19);
insert into detalii_film values(3,'Fast and Furoius II','Thriller',107,2003,'Paul Walker','2D',12,21);
insert into detalii_film values(4,'John Wick','Thriller',101,2014,'Keanu Reeves','3D',15,19);
insert into detalii_film values(5,'Titanic','Drama',195,1997,'Kate Winslet','2D',12,22);
insert into detalii_film values(6,'Matrix','SF',136,1999,'Keanu Reeves','2D',12,23);
insert into detalii_film values(7,'Home Alone','Comedie',103,1990,'Macaulay Culkin','2D',12,17);
insert into detalii_film values(8,'Jack Reacher','Thriller',130,2012,'Tom Cruise','3D',15,18);
insert into detalii_film values(9,'Fifty Shades of Grey','Romance',125,2015,'Dakota Johnson','2D',18,21);
insert into detalii_film values(10,'The nun','Horror',96,2018,'Taissa Farmiga','2D',15,18);

insert into particularitati values(1,2787965087,'James Cameron','Century Fox');
insert into particularitati values(2,207283925,'Rob Cohen','Universal Pictures');
insert into particularitati values(3,236350661,'John Singleton','Universal Pictures');
insert into particularitati values(4,86000000,'Chad Stahelsk','Thunder Road Pictures');
insert into particularitati values(5,2187000000,'James Cameron','Century Fox');
insert into particularitati values(6,463517383,'Fratii Wachowski','Warner Bros Pictures');
insert into particularitati values(7,476684675,'Chris Columbus','Century Fox');
insert into particularitati values(8,218300000,'Christopher McQuarrie','Paramount Pictures');
insert into particularitati values(9,569700000,'Sam Taylor','Universal Pictures');
insert into particularitati values(10,356600000,'Corin Hardy','Warner Bros');


insert into film_particularitati values (1,1);
insert into film_particularitati values (2,2);
insert into film_particularitati values (3,3);
insert into film_particularitati values (4,4);
insert into film_particularitati values (5,5);
insert into film_particularitati values (6,6);
insert into film_particularitati values (7,7);
insert into film_particularitati values (8,8);
insert into film_particularitati values (9,9);
insert into film_particularitati values (10,10);

insert into contracte_inchirieri values(221,'12-JUL-2021','28-JUL-2021',21,2,3);
insert into contracte_inchirieri values(223,'21-JAN-2022','2-FEB-2022',17,1,7);
insert into contracte_inchirieri values(422,'4-DEC-2022','23-DEC-2022',24,4,1);
insert into contracte_inchirieri values(231,'2-JAN-2023','9-JAN-2023',21,3,9);
insert into contracte_inchirieri values(300,'27-NOV-2022','7-DEC-2022',18,5,10);
