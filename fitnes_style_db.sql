-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-01-2024 a las 01:26:17
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `fitnes_style_db`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_product` (IN `id_product` INT(11), IN `quantity_product` INT(5))   UPDATE product SET quantity = quantity + quantity_product WHERE id = id_product$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `process_sale` (IN `client_id` INT, IN `product1_id` INT, IN `product1_quantity` INT, IN `product2_id` INT, IN `product2_quantity` INT, IN `product3_id` INT, IN `product3_quantity` INT, IN `product4_id` INT, IN `product4_quantity` INT, IN `product5_id` INT, IN `product5_quantity` INT, IN `is_paid_in_full` BOOLEAN, IN `payment_amount` DECIMAL(10,2))   BEGIN
    DECLARE total_cost DECIMAL(10, 2);
    DECLARE total_price DECIMAL(10, 2);
    DECLARE next_sale_id INT;
    
    -- Calcular el costo y el precio total de los productos vendidos
    SET total_cost = (
        SELECT SUM(p.cost * sp.quantity)
        FROM product p
        JOIN (
            SELECT product1_id AS id, product1_quantity AS quantity
            UNION ALL
            SELECT product2_id, product2_quantity
            UNION ALL
            SELECT product3_id, product3_quantity
            UNION ALL
            SELECT product4_id, product4_quantity
            UNION ALL
            SELECT product5_id, product5_quantity
        ) sp ON p.id = sp.id
    );
    
    SET total_price = (
        SELECT SUM(p.price * sp.quantity)
        FROM product p
        JOIN (
            SELECT product1_id AS id, product1_quantity AS quantity
            UNION ALL
            SELECT product2_id, product2_quantity
            UNION ALL
            SELECT product3_id, product3_quantity
            UNION ALL
            SELECT product4_id, product4_quantity
            UNION ALL
            SELECT product5_id, product5_quantity
        ) sp ON p.id = sp.id
    );
    
    -- Obtener el próximo valor para 'id_sale'
    SET next_sale_id = (
        SELECT IFNULL(MAX(id_sale), 0) + 1
        FROM sale
    );
    
    -- Insertar la venta en la tabla 'sale'
    INSERT INTO sale (id, id_client, date, total_price, total_cost, total_profit)
    VALUES (next_sale_id, client_id, CURRENT_DATE(), total_price, total_cost, total_price - total_cost);
    
    -- Insertar los productos vendidos en la tabla 'sale_product'
    INSERT INTO sale_product (id_sale, id_product, quantity)
    SELECT next_sale_id, sp.id, sp.quantity
    FROM (
        SELECT product1_id AS id, product1_quantity AS quantity
        UNION ALL
        SELECT product2_id, product2_quantity
        UNION ALL
        SELECT product3_id, product3_quantity
        UNION ALL
        SELECT product4_id, product4_quantity
        UNION ALL
        SELECT product5_id, product5_quantity
    ) sp
    WHERE sp.id IS NOT NULL;
    
    -- Registrar el pago si se pagó en su totalidad
    IF is_paid_in_full THEN
        INSERT INTO payments (total_payment, date)
        VALUES (payment_amount, CURRENT_DATE());
    ELSE
        -- Calcular el monto pendiente (deuda)
        SET @debt_amount = total_price - payment_amount;
        
        -- Registrar el pago parcial en la tabla 'payments'
        INSERT INTO payments (total_payment, date)
        VALUES (payment_amount, CURRENT_DATE());
        
        -- Registrar el monto pendiente en la tabla 'debt'
        INSERT INTO debt (id_client, total_debt, date, comments)
        VALUES (client_id, @debt_amount, CURRENT_DATE(), 'Monto pendiente');
    END IF;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `client`
--

CREATE TABLE `client` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `colony` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `cellphone` varchar(15) DEFAULT NULL,
  `debt` int(11) NOT NULL,
  `debt_comment` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `client`
--

INSERT INTO `client` (`id`, `name`, `lastname`, `colony`, `address`, `cellphone`, `debt`, `debt_comment`) VALUES
(1, 'Carlos', 'lopez', '', '', '4331027765', 0, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `profit` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `product`
--

INSERT INTO `product` (`id`, `name`, `description`, `quantity`, `price`, `cost`, `profit`) VALUES
(1, 'queso 1', '', 10, 1000.00, 500.00, 500.00),
(2, 'queso 2', '', 10, 1000.00, 500.00, 500.00),
(3, 'queso 3', '', 10, 1000.00, 500.00, 500.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sale`
--

CREATE TABLE `sale` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `id_client` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sale`
--

INSERT INTO `sale` (`id`, `date`, `id_client`) VALUES
(1, '2023-10-24', 1);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `sales_info`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `sales_info` (
`sale_number` int(11)
,`sale_date` date
,`products_sold` mediumtext
,`total_cost` decimal(42,0)
,`total_price` decimal(42,0)
,`total_profit` decimal(43,0)
,`client_name` varchar(511)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `sales_info_daily`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `sales_info_daily` (
`sale_number` int(11)
,`sale_date` date
,`products_sold` mediumtext
,`total_cost` decimal(42,0)
,`total_price` decimal(42,0)
,`total_profit` decimal(43,0)
,`client_name` varchar(511)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sale_product`
--

CREATE TABLE `sale_product` (
  `id` int(11) NOT NULL,
  `id_sale` int(11) DEFAULT NULL,
  `id_product` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `final_price` int(11) NOT NULL,
  `final_cost` int(11) NOT NULL,
  `final_profit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sale_product`
--

INSERT INTO `sale_product` (`id`, `id_sale`, `id_product`, `quantity`, `final_price`, `final_cost`, `final_profit`) VALUES
(1, 1, 1, 4, 1000, 500, 500),
(2, 1, 2, 1, 1000, 500, 500),
(3, 1, 3, 1, 1000, 500, 500);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `stock`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `stock` (
`product_id` int(11)
,`product_name` varchar(255)
,`product_description` text
,`total_pieces_in_stock` decimal(33,0)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `sales_info`
--
DROP TABLE IF EXISTS `sales_info`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `sales_info`  AS SELECT `s`.`id` AS `sale_number`, `s`.`date` AS `sale_date`, group_concat(concat(`p`.`name`,' (',`sp`.`quantity`,')') order by `sp`.`id` ASC separator '; ') AS `products_sold`, sum(`sp`.`final_cost` * `sp`.`quantity`) AS `total_cost`, sum(`sp`.`final_price` * `sp`.`quantity`) AS `total_price`, sum((`sp`.`final_price` - `sp`.`final_cost`) * `sp`.`quantity`) AS `total_profit`, concat(`c`.`name`,' ',`c`.`lastname`) AS `client_name` FROM (((`sale` `s` join `client` `c` on(`s`.`id_client` = `c`.`id`)) join `sale_product` `sp` on(`s`.`id` = `sp`.`id_sale`)) join `product` `p` on(`sp`.`id_product` = `p`.`id`)) GROUP BY `s`.`id`, `s`.`date`, `c`.`name`, `c`.`lastname` ;

-- --------------------------------------------------------

--
-- Estructura para la vista `sales_info_daily`
--
DROP TABLE IF EXISTS `sales_info_daily`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `sales_info_daily`  AS SELECT `s`.`id` AS `sale_number`, `s`.`date` AS `sale_date`, group_concat(concat(`p`.`name`,' (',`sp`.`quantity`,')') order by `sp`.`id` ASC separator '; ') AS `products_sold`, sum(`sp`.`final_cost` * `sp`.`quantity`) AS `total_cost`, sum(`sp`.`final_price` * `sp`.`quantity`) AS `total_price`, sum((`sp`.`final_price` - `sp`.`final_cost`) * `sp`.`quantity`) AS `total_profit`, concat(`c`.`name`,' ',`c`.`lastname`) AS `client_name` FROM (((`sale` `s` join `client` `c` on(`s`.`id_client` = `c`.`id`)) join `sale_product` `sp` on(`s`.`id` = `sp`.`id_sale`)) join `product` `p` on(`sp`.`id_product` = `p`.`id`)) WHERE `s`.`date` = curdate() GROUP BY `s`.`id`, `s`.`date`, `c`.`name`, `c`.`lastname` ;

-- --------------------------------------------------------

--
-- Estructura para la vista `stock`
--
DROP TABLE IF EXISTS `stock`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `stock`  AS SELECT `p`.`id` AS `product_id`, `p`.`name` AS `product_name`, `p`.`description` AS `product_description`, `p`.`quantity`- coalesce(sum(`sp`.`quantity`),0) AS `total_pieces_in_stock` FROM (`product` `p` left join `sale_product` `sp` on(`p`.`id` = `sp`.`id_product`)) GROUP BY `p`.`id`, `p`.`name`, `p`.`description`, `p`.`quantity` ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `sale`
--
ALTER TABLE `sale`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_client` (`id_client`);

--
-- Indices de la tabla `sale_product`
--
ALTER TABLE `sale_product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_sale` (`id_sale`,`id_product`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `client`
--
ALTER TABLE `client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `sale`
--
ALTER TABLE `sale`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `sale_product`
--
ALTER TABLE `sale_product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
