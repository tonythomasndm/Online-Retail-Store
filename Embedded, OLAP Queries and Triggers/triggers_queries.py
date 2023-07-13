import mysql.connector
mydb=mysql.connector.connect(
    host='127.0.0.1',
    database="onlineretailstore",
    user='root',
    password='tony022002@Kuku'
)
cursor=mydb.cursor()

while(True):
    print("""Choose Trigger:
    1.Trigger to update the total amount of a cart when a new cart_item is added by the customer
    2.Checks stock value before adding a new cart_item, useful when a customer wishes to add a new item to their cart, there will be an automatic check imposed which would ensure that the item is added only if there is enough stock""")

    trigger_num=int(input())
        #Trigger 1
    if(trigger_num==1):
        print("""Choose trigger function
    1.Insert Trigger
    2.Drop trigger
    3.Test trigger""")
        query_num=int(input())
        if(query_num==1):
            print("Started with the trigger execution : ")
            print("Executing the first trigger... ")
            cmd="""DELIMITER $$
                    CREATE TRIGGER cart_item_add_and_cart_total_amount_update
                    AFTER INSERT
                    ON cart_item
                    FOR EACH ROW
                    BEGIN
                    UPDATE cart
                    SET cart.cart_total_amount= cart.cart_total_amount + ((SELECT P.price FROM
                    product P WHERE P.product_id = NEW.product_id) * NEW.quantity)
                    WHERE cart.cart_id= NEW.cart_id;
                    END $$
                    DELIMITER ;"""
            cursor.execute(cmd);
            print("""Trigger to update the total amount of a cart when a new cart_item is added by
            the customer...\nTrigger executed successfully""")

        elif(query_num==2):
            cursor.execute("""DROP TRIGGER onlineretailstore.cart_item_check_if_quantity_exists;""")
        
        elif(query_num==3):
            cursor.execute("""INSERT INTO cart_item
                                (cart_id, product_id, quantity)
                                VALUES
                                ('CART447', 'PROD268', 325);""")
            

        #Trigger 2
    elif(trigger_num==2):
        print("""Choose trigger function
    1.Insert Trigger
    2.Drop trigger
    3.Test trigger""")
        query_num=int(input())
        if(query_num==1):
            print("Started with the trigger execution : ")
            print("Executing the first trigger... ")
            cmd="""DELIMITER $$
                    CREATE TRIGGER cart_item_check_if_quantity_exists
                    BEFORE INSERT
                    ON cart_item
                    FOR EACH ROW
                    BEGIN
                    IF (NEW.quantity >= (SELECT P.stock FROM product P WHERE
                    P.product_id = NEW.product_id))
                    THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Not enough stock';
                    END IF;
                    END $$
                    DELIMITER ;"""
            cursor.execute(cmd);
            print("""Trigger to check stock value before adding a new cart_item, useful when a customer
    wishes to add a new item to their cart...\nTrigger executed successfully""")

        elif(query_num==2):
            cursor.execute("""DROP TRIGGER onlineretailstore.cart_item_check_if_quantity_exists;""")
        
        elif(query_num==3):
            cursor.execute("""INSERT INTO cart_item
                                (cart_id, product_id, quantity)
                                VALUES
                                ('CART447', 'PROD268', 325);""")
    else:
        print("Thank you")
        break;

