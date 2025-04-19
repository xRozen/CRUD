INSERT INTO alumno (nombre_alm, ap_paterno, ap_materno, correo_alm, contrasena, semestre_alm, num_cuenta)
VALUES ('Carlos', 'Ramírez', 'Gómez', 'carlos.ramirez@aragon.unam.mx', 'contrasena123', 3, '321456789'),
('María', 'López', 'Hernández', 'maria.lopez@aragon.unam.mx', 'maria2025', 5, '321456790'),
('Luis', '', 'Martínez', 'luis.martinez@aragon.unam.mx', 'luispass', 2, '321456791'),
('Ana', 'García', 'Torres', 'ana.garcia@aragon.unam.mx', 'ana1234', 4, '321456792'),
('Miguel', '', 'Flores', 'miguel.flores@aragon.unam.mx', 'miguel2024', 6, '321456793'),
('Monica', 'Canal', 'Peña', 'monica.pena@aragon.unam.mx', 'monica2321', 9, '296482047');

INSERT INTO profesor (nombre_prof, ap_paterno, ap_materno, correo_prof, rfc)
VALUES ('Matin', 'Ordoñez', 'Rosales', 'martinordonez7e1@aragon.unam.mx', 'ORAM7208010X1'),
('Sergio', 'Hernandez', 'López', 'sergiohernandezhel@aragon.unam.mx', 'HELS7209019S3'),
('Aarón', 'Velasco', 'Agustín', 'aaronvelazcovea@aragon.unam.mx', 'VEAA7602129T2'),
('Gerardo', 'González', 'Hernández', 'gerardogonzalezgoh@aragon.unam.mx', 'GOHG7508159H7'),
('Leobardo', 'Hernández', 'Audelo', 'leoher34@aragon.unam.mx', 'HEAL7611251J9');

INSERT INTO asignatura (nombre_asg, clave_asg, semestre_asg, creditos_asg, laboratorio, optativa)
VALUES ('Algebra', 1110, 1, 09, FALSE, FALSE),
('Electricidad y Magnetismo', 0071, 3, 11, TRUE, FALSE),
('Lenguajes Formales y Automatas', 0442, 5, 08, FALSE, FALSE),
('Instrumentación y Control', 1627, 7, 08, FALSE, TRUE),
('Seminario de Ingeniería en Computación', 0018, 9, 08, FALSE, TRUE);

INSERT INTO salon (nombre_sln, cupo)
VALUES ('A214', 45),
('A503', 25),
('A325', 30),
('A816', 20),
('A11205', 30);

INSERT INTO dia_sem (dia)
VALUES ('Lunes'),
('Martes'),
('Miércoles'),
('Jueves'),
('Viernes'),
('Sábado');

INSERT INTO horario (id_asg, id_prof, id_sln, hrs_inicio, hrs_fin, id_dia_sem)
VALUES (3, 2, 1, '13:00', '15:00', 2),
(3, 5, 4, '12:00', '14:00', 5),
(1, 3, 5, '15:30', '17:00', 1),
(1, 4, 2, '10:00', '12:00', 3),
(5, 1, 3, '18:00', '20:00', 4);

INSERT INTO inscripcion (id_alm, id_hrs)
VALUES (2, 1),
(4, 3),
(1, 5),
(3, 2),
(5, 4);