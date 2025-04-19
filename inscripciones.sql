DROP DATABASE IF EXISTS inscripciones;
CREATE DATABASE IF NOT EXISTS inscripciones;
USE inscripciones;

CREATE TABLE alumno(
	id_alm			INTEGER NOT NULL AUTO_INCREMENT,
    nombre_alm		VARCHAR (50) NOT NULL,
    ap_paterno		VARCHAR (50),
    ap_materno		VARCHAR (50) NOT NULL,
    correo_alm		VARCHAR (50) NOT NULL UNIQUE,
    contrasena		VARCHAR (15) NOT NULL,
    semestre_alm	TINYINT NOT NULL,
    num_cuenta		INTEGER NOT NULL UNIQUE,
    
    PRIMARY KEY (id_alm)
) ENGINE=InnoDB;

CREATE TABLE profesor(
	id_prof			INTEGER NOT NULL AUTO_INCREMENT,
    nombre_prof		VARCHAR (50) NOT NULL,
    ap_paterno		VARCHAR (50),
    ap_materno		VARCHAR (50) NOT NULL,
    correo_prof		VARCHAR (50) NOT NULL UNIQUE,
    rfc				VARCHAR (13) NOT NULL UNIQUE,
    
    PRIMARY KEY (id_prof)
) ENGINE=InnoDB;

CREATE TABLE asignatura(
	id_asg			INTEGER NOT NULL AUTO_INCREMENT,
    nombre_asg		VARCHAR (100) NOT NULL,
    clave_asg		SMALLINT NOT NULL UNIQUE,
    semestre_asg	TINYINT NOT NULL,
    creditos_asg	TINYINT NOT NULL,
    laboratorio		BOOLEAN NOT NULL DEFAULT FALSE,
    optativa		BOOLEAN NOT NULL DEFAULT FALSE,
    
    PRIMARY KEY (id_asg)
) ENGINE=InnoDB;

CREATE TABLE salon(
	id_sln			INTEGER NOT NULL AUTO_INCREMENT,
    nombre_sln		VARCHAR (10) NOT NULL UNIQUE,
    cupo			TINYINT NOT NULL,
    
    PRIMARY KEY (id_sln)
) ENGINE=InnoDB;

CREATE TABLE dia_sem(
	id_dia_sem		INTEGER NOT NULL AUTO_INCREMENT,
    dia				VARCHAR (10) NOT NULL UNIQUE,
    
    PRIMARY KEY (id_dia_sem)
) ENGINE=InnoDB;

CREATE TABLE horario(
	id_hrs			INTEGER NOT NULL AUTO_INCREMENT,
    id_asg			INTEGER NOT NULL,
    id_prof			INTEGER NOT NULL,
    id_sln			INTEGER NOT NULL,
    hrs_inicio		TIME NOT NULL,
    hrs_fin			TIME NOT NULL,
    id_dia_sem		INTEGER NOT NULL,
    
    PRIMARY KEY (id_hrs),
    FOREIGN KEY (id_asg) REFERENCES asignatura (id_asg),
    FOREIGN KEY (id_prof) REFERENCES profesor (id_prof),
    FOREIGN KEY (id_sln) REFERENCES salon (id_sln),
    FOREIGN KEY (id_dia_sem) REFERENCES dia_sem (id_dia_sem)
) ENGINE=InnoDB;

CREATE TABLE inscripcion(
	id_insc			INTEGER NOT NULL AUTO_INCREMENT,
    id_alm			INTEGER NOT NULL,
    id_hrs			INTEGER NOT NULL,
    
    PRIMARY KEY (id_insc),
    FOREIGN KEY (id_alm) REFERENCES alumno (id_alm),
    FOREIGN KEY (id_hrs) REFERENCES horario (id_hrs)
) ENGINE=InnoDB;