#Query1
SELECT C.first_name, C.last_name
FROM Customer C, Authentication_credentials A
WHERE A.login_id=78793 AND A.password='PtSHC6' AND C.customer_id=A.customer_id;

#Query2
SELECT P.name, P.description, P.price
FROM Product P 
WHERE P.name LIKE "%Wine%";

#Query3
SELECT OI.*, O.order_date, O.order_status
FROM Order_item OI, `Order` O
WHERE OI.order_id = O.order_id AND O.order_id='ORDER117';

#Query4
UPDATE Authentication_credentials A
SET A.password="newPwd"
WHERE A.login_id=78793 AND A.password='PtSHC6' AND A.customer_id='CUST001';

UPDATE Authentication_credentials A
SET A.password="PtSHC6"
WHERE A.login_id=78793 AND A.password='newPwd' AND A.customer_id='CUST001';

#Query5
DELETE FROM cart_item C
WHERE C.cart_id="CART447" AND C.product_id="PROD248";

#Query6
INSERT INTO cart_item 
(cart_id, product_id, quantity)
VALUES 
('CART447', 'PROD248', 35);

#Query7
SELECT C.first_name, O.order_id, O.order_date, O.net_amount, CO.percentage_discount
FROM Customer C, `Order` O, Coupon CO
WHERE C.customer_id = O.customer_id 
AND O.coupon_id = CO.coupon_id
AND O.coupon_id 
IN (SELECT COU.coupon_id 
FROM Coupon COU
WHERE COU.percentage_discount >=20);

#Query8
UPDATE Cart_item CI INNER JOIN Customer C ON CI.cart_id = C.cart_id
SET CI.quantity = CI.quantity + 1
WHERE CI.product_id = 'PROD124'
AND C.customer_id ='CUST141';

UPDATE Cart_item CI INNER JOIN Customer C ON CI.cart_id = C.cart_id
SET CI.quantity = CI.quantity - 1
WHERE CI.product_id = 'PROD124'
AND C.customer_id ='CUST141';

#Query9
SELECT SUM(O.net_amount)
FROM `Order` O, Customer C
WHERE C.customer_id = O.customer_id
AND C.customer_id = 'CUST408';

#Query10
SELECT C.customer_id, C.first_name, C.last_name, SUM(O.net_amount)
FROM `Order` O, Customer C
WHERE O.customer_id = C.customer_id
GROUP BY O.customer_id
HAVING SUM(O.net_amount) > 7000
ORDER BY SUM(O.net_amount) desc;

#Query11
SELECT C.customer_id, C.first_name, C.last_name, AVG(O.net_amount)
FROM `Order` O, Customer C
WHERE O.customer_id = C.customer_id
GROUP BY O.customer_id
ORDER BY AVG(O.net_amount) asc;

#Query12
SELECT C.customer_id, C.first_name, C.last_name, MAX(O.net_amount)
FROM `Order` O, Customer C
WHERE O.customer_id = C.customer_id AND C.customer_id = 'CUST408';








