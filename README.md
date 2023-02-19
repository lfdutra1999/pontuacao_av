# pontuacao_av


docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=meuovo -e MYSQL_DATABASE=rpmesports -e MYSQL_USER=rpm -e MYSQL_PASSWORD=meuovo mysql:latest


"INSERT INTO grid_pontos (grid_id, posicao, pontos) VALUES    (1, 1, 25),    (1, 2, 20),    (1, 3, 18),    (1, 4, 16),    (1, 5, 14),    (1, 6, 12),    (2, 1, 29),    (2, 2, 25), (2, 3, 20),    (1, 4, 18), (1, 5, 16), (1, 6, 14), (3, 1, 35), (3, 2, 29), (3, 3, 25), (1, 4, 22), (1, 5, 20), (1, 6, 18)"