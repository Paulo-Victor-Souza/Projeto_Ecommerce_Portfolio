

-- =====================================================
-- PROJETO: E-COMMERCE SALES ANALYTICS
-- Base de dados: Olist Brazilian E-commerce
-- Objetivo: Analisar encomendas, vendas, produtos,
-- clientes, pagamentos e satisfação.
-- =====================================================


-- ANÁLISE 1: Consultar os primeiros 10 pedidos

SELECT *
FROM olist_orders_dataset
LIMIT 10;


-- ANÁLISE 2: Contar o número total de pedidos

SELECT
    COUNT(*) AS total_pedidos
FROM olist_orders_dataset;


-- ANÁLISE 3: Distribuição dos pedidos por estado

SELECT
    order_status,
    COUNT(*) AS quantidade
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY quantidade DESC;


-- ANÁLISE 4: Percentagem de pedidos por estado

SELECT
    order_status,
    COUNT(*) AS quantidade,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM olist_orders_dataset),
        2
    ) AS percentagem
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY quantidade DESC;


-- ANÁLISE 5: Relacionar pedidos com os artigos

SELECT
    o.order_id,
    o.order_status,
    i.order_item_id,
    i.product_id,
    i.price,
    i.freight_value
FROM olist_orders_dataset AS o
INNER JOIN olist_order_items_dataset AS i
    ON o.order_id = i.order_id
LIMIT 10;


-- ANÁLISE 6: Valor total dos artigos e dos portes

SELECT
    ROUND(SUM(price), 2) AS valor_total_artigos,
    ROUND(SUM(freight_value), 2) AS valor_total_portes,
    ROUND(SUM(price + freight_value), 2) AS valor_total_com_portes
FROM olist_order_items_dataset;


-- ANÁLISE 7: As 10 categorias de produtos com maior valor em artigos

SELECT
    p.product_category_name AS categoria,
    COUNT(*) AS quantidade_artigos,
    ROUND(SUM(i.price), 2) AS valor_total_artigos
FROM olist_order_items_dataset AS i
INNER JOIN olist_products_dataset AS p
    ON i.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY valor_total_artigos DESC
LIMIT 10;


-- ANÁLISE 8: Os 10 estados com mais clientes

SELECT
    customer_state AS estado,
    COUNT(*) AS total_clientes
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY total_clientes DESC
LIMIT 10;


-- ANÁLISE 9: Número de encomendas por estado dos clientes

SELECT
    c.customer_state AS estado,
    COUNT(*) AS total_encomendas
FROM olist_orders_dataset AS o
INNER JOIN olist_customers_dataset AS c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_encomendas DESC
LIMIT 10;


-- ANÁLISE 10: Verificar total de encomendas e clientes associados

SELECT
    COUNT(*) AS total_encomendas,
    COUNT(DISTINCT customer_id) AS clientes_associados
FROM olist_orders_dataset;


-- ANÁLISE 11: Verificar correspondências entre encomendas e clientes

SELECT
    COUNT(*) AS total_linhas,
    COUNT(DISTINCT o.order_id) AS encomendas_distintas,
    COUNT(c.customer_id) AS correspondencias_clientes
FROM olist_orders_dataset AS o
INNER JOIN olist_customers_dataset AS c
    ON o.customer_id = c.customer_id;


-- ANÁLISE 12: Total de registos e valor dos pagamentos

SELECT
    COUNT(*) AS total_registos_pagamento,
    ROUND(SUM(payment_value), 2) AS valor_total_pagamentos
FROM olist_order_payments_dataset;


-- ANÁLISE 13: Analisar os métodos de pagamento

SELECT
    payment_type AS metodo_pagamento,
    COUNT(*) AS total_registos,
    ROUND(SUM(payment_value), 2) AS valor_total
FROM olist_order_payments_dataset
GROUP BY payment_type
ORDER BY valor_total DESC;


-- ANÁLISE 14: Distribuição das avaliações dos clientes

SELECT
    review_score AS nota,
    COUNT(*) AS total_avaliacoes
FROM olist_order_reviews_dataset
GROUP BY review_score
ORDER BY review_score DESC;


-- ANÁLISE 15: Média de satisfação dos clientes

SELECT
    ROUND(AVG(review_score), 2) AS media_avaliacoes,
    COUNT(*) AS total_avaliacoes
FROM olist_order_reviews_dataset;


-- ANÁLISE 16: Comparar avaliações registadas com encomendas avaliadas

SELECT
    COUNT(*) AS total_registos_avaliacao,
    COUNT(DISTINCT order_id) AS encomendas_com_avaliacao
FROM olist_order_reviews_dataset;


-- ANÁLISE 17: Identificar encomendas com várias avaliações

SELECT
    order_id,
    COUNT(*) AS total_avaliacoes
FROM olist_order_reviews_dataset
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY total_avaliacoes DESC
LIMIT 10;


-- ANÁLISE 18: Identificar encomendas sem avaliação

SELECT
    COUNT(*) AS encomendas_sem_avaliacao
FROM olist_orders_dataset AS o
LEFT JOIN olist_order_reviews_dataset AS r
    ON o.order_id = r.order_id
WHERE r.order_id IS NULL;


-- ANÁLISE 19: Comparar datas de entrega com datas previstas

SELECT
    COUNT(*) AS total_encomendas_entregues,
    SUM(
        CASE
            WHEN order_delivered_customer_date
                 <= order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS entregues_no_prazo,
    SUM(
        CASE
            WHEN order_delivered_customer_date
                 > order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS entregues_com_atraso
FROM olist_orders_dataset
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;

  
-- ANÁLISE 20: Calcular o atraso médio das entregas, em dias

SELECT
    COUNT(*) AS encomendas_com_atraso,
    ROUND(
        AVG(
            julianday(order_delivered_customer_date)
            - julianday(order_estimated_delivery_date)
        ),
        2
    ) AS media_dias_atraso,
    MAX(
        ROUND(
            julianday(order_delivered_customer_date)
            - julianday(order_estimated_delivery_date),
            2
        )
    ) AS maior_atraso_dias
FROM olist_orders_dataset
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
  AND order_delivered_customer_date > order_estimated_delivery_date;

  
-- ANÁLISE 22: Consultar os primeiros 10 vendedores

SELECT *
FROM olist_sellers_dataset
LIMIT 10;


-- ANÁLISE 23: Contar o total de vendedores

SELECT
    COUNT(*) AS total_vendedores
FROM olist_sellers_dataset;


-- ANÁLISE 24: Consultar os primeiros 10 registos de geolocalização

SELECT *
FROM olist_geolocation_dataset
LIMIT 10;


-- ANÁLISE 25: Contar os registos de geolocalização

SELECT
    COUNT(*) AS total_registos_geolocalizacao
FROM olist_geolocation_dataset;
