-- creates a trigger that decreases the quantity of an item after adding a new order.
DELIMITER //
CREATE TRIGGER after_order_insert AFTER INSERT ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
//

DELIMITER ;
