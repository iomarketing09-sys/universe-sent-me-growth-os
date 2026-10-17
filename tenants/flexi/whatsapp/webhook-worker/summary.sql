-- Reporte de la observación (2 semanas).
SELECT 'mensajes entrantes' AS metrica, COUNT(*) AS valor FROM events WHERE direction = 'in'
UNION ALL SELECT 'respuestas de la app', COUNT(*) FROM events WHERE direction = 'out_app'
UNION ALL SELECT 'contactos únicos', COUNT(DISTINCT contact_hash) FROM events WHERE direction = 'in'
UNION ALL SELECT 'conversaciones de 0 a 1 día', COUNT(DISTINCT substr(received_at, 1, 10) || contact_hash) FROM events WHERE direction = 'in';

SELECT intent, COUNT(*) AS n
FROM events WHERE direction = 'in'
GROUP BY intent ORDER BY n DESC;

SELECT substr(received_at, 1, 10) AS dia, direction, COUNT(*) AS n
FROM events GROUP BY dia, direction ORDER BY dia;
