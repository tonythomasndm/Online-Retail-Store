import mysql.connector
from datetime import datetime
from datetime import datetime, date, timedelta

mydb=mysql.connector.connect(
    host='127.0.0.1',
    database="onlineretailstore",
    user='root',
    password='tony022002@Kuku'
)

wallet = 20000
cursor=mydb.cursor()
# mydb.get_autocommit()
mydb.autocommit=True
# mydb.get_autocommit()


def general_menu_admin():
    print("\nChoose the way to enter as an admin : \n1. LogIn as Admin\n2. Sign Up as a new Admin\n3. Exit to Main Menu")
def admin_process(admin_id):
    while(True):
        print("\nMenu :\n1.Add a category\n2.Delete a category\n3.Add a product\n4.Delete a product\n5.Set discount on a product\n6.Change category of a product\n7.Update details on a category\n8.Update details on a product\n9.Sales Analysis\n10.Back to Previous menu\n")
        choice=int(input("\nEnter your choice :"))
        if(choice==1):
            print("Enter the following category details :")
            cmd="""SELECT COUNT(*) FROM category;"""
            cursor.execute(cmd)
            number=int(cursor.fetchone()[0])+1
            name=input("Enter the category name :")
            cmd=f""" INSERT INTO Category (category_id, admin_id, category_name) VALUES('CATEGORY{number}','{admin_id}','{name}');"""
            cursor.execute(cmd)
            print("New category with CategoryId - CATEGORY"+str(number)+" added successfully")
        elif(choice==2):
            print("Enter the following category details :")
            category_id=input("Enter the category ID of the category to be deleted:")
            cmd=f""" DELETE FROM category C WHERE C.category_id='{category_id}';"""
            #trigger needed- due to a category deleted - all products deleted then all cart items deleted- cart_total_updated
            cursor.execute(cmd);
            print("Category with CategoryId -",category_id," deleted successfully")
        elif(choice==3):
            category_id=input("Choose the category where it is to be inserted :\nEnter the Category ID:")
            print("Enter the following product details")
            
            cmd="""SELECT COUNT(*) FROM product;"""
            cursor.execute(cmd)
            number=int(cursor.fetchone()[0])+1
            name=input("Name : ")
            description=input("Description : ")
            price=int(input("Price : Rs"))
            stock=int(input("Stock : "))
            discount=int(input("Discount Offered(in %) :"))
            product_id='PROD'+str(number)
            cmd=f"""INSERT INTO Product (product_id, category_id, admin_id, name, description, price, stock, discount)
                    VALUES ('{product_id}','{category_id}','{admin_id}','{name}','{description}',{price},{stock},{discount});"""
            cursor.execute(cmd)
            print("New product with ProductId - PROD"+str(number)+f" under CategoryId-{category_id} added successfully")
        elif(choice==4):
            print("Enter the following product details :")
            product_id=input("Enter the product ID of the product to be deleted:")
            cmd=f""" DELETE FROM Product P WHERE P.product_id='{product_id}';"""
            #trigger needed- due to a productdeleted - all cart items deleted- cart_total_updated
            cursor.execute(cmd);
            print("Product with ProductId -",product_id," deleted successfully")
        elif(choice==5):
            print("Enter the following product details :")
            product_id=input("Enter the product ID of the product whose discount is to be set:")
            discount=int(input("Enter the discount rate(in %) :"))
            cmd=f"""UPDATE Product P
                    SET P.discount={discount}
                    WHERE P.product_id='{product_id}'"""
            cursor.execute(cmd)
            print("Discount Set on the Product with ProductId -",product_id)
        elif(choice==6):
            print("Enter the following product details :")
            product_id=input("Enter the product ID of the product whose discount is to be set:")
            category_id=input("Enter the categoryID of the category to be part of:")
            cmd=f"""UPDATE Product P
                    SET P.category_id='{category_id}', P.admin_id='{admin_id}'
                    WHERE P.product_id='{product_id}'"""
            cursor.execute(cmd)
            print("CategoryId changed on the Product with ProductId -",product_id)
        elif(choice==7):
            print("Enter the following category details :")
            category_id=input("Enter the category ID of the category to be updated:")
            name=input("Enter the name of the category to be set :")
            cmd=f""" UPDATE category C 
                    SET C.category_name='{name}', C.admin_id='{admin_id}'
                    WHERE C.category_id='{category_id}';"""
            cursor.execute(cmd)
            print("Category Name updated for Category Id -",category_id)
        elif(choice==8):
            print("Enter the following product details :")
            product_id=input("Enter the product ID of the product whose details is/are to be set:")
            print("Choose the parameter of the product to be updated\n1.Name\n2.Description\n3.Price\n4.Stock")
            print("Suppose to update the name and description, you can enter : 12 and similarly if name, price and stock, you can enter : 134")
            choice=input("Enter the choices :")
            if("1" in choice):
                name=input("Enter the name :")
                cmd=f"""UPDATE Product P
                        SET P.name='{name}', P.admin_id='{admin_id}'
                        WHERE P.product_id='{product_id}'"""
                cursor.execute(cmd)
                print("Name Updated!!")
            if("2" in choice):
                description=input("Enter the description :")
                cmd=f"""UPDATE Product P
                        SET P.description='{description}', P.admin_id='{admin_id}'
                        WHERE P.product_id='{product_id}'"""
                cursor.execute(cmd)
                print("Description Updated!!")
            if("3" in choice):
                price=int(input("Enter the price : Rs"))
                cmd=f"""UPDATE Product P
                        SET P.price={price}, P.admin_id='{admin_id}'
                        WHERE P.product_id='{product_id}'"""
                cursor.execute(cmd)
                print("Price Updated!!")
            if("4" in choice):
                stock=int(input("Enter the stock :"))
                cmd=f"""UPDATE Product P
                        SET P.stock={stock}, P.admin_id='{admin_id}'
                        WHERE P.product_id='{product_id}'"""
                cursor.execute(cmd)
                print("Stock Updated!!")
        elif(choice==9):
            print("SALES ANALYSIS")
            print("""\nChoose OLAP query:
1. An OLAP query that gives the total number of items (products*quantity) in that category as well as the net monetary amount present in that category. It adds the stock quantities of all the products belonging to that category and also multiplies the price with the stock and adds that.
\n2. An OLAP query to return the total amount spent by customers till now on the shopping platform, it also gives the total amount spent on all orders till now
\n3. An OLAP query to return the total number of products in a category and the total number of items present in that category.""")
            print("\n")    
            query_num=int(input())

            #OLAP Query 1
            if(query_num==1):
                cmd="""SELECT COALESCE(category_id, 'All categories') AS 'Category Id', SUM(stock) AS
                        'Number of Quantities in this category', SUM(price*stock) AS 'Total Cost of this Category'
                        FROM product
                        GROUP BY (category_id) WITH ROLLUP;"""
                cursor.execute(cmd);
                for i in cursor:
                    print("Category ID :",i[0])
                    print("Number of quantities :",i[1]);
                    print("Total Cost of this Category : Rs",i[2])
                    print()
            
            #OLAP Query 3
            elif(query_num==2):
                cmd="""SELECT COALESCE(O.customer_id, 'All customers') AS 'CustomerID',
                    SUM(O.net_amount) AS 'Total amount spent'
                    FROM `Order` O
                    GROUP BY O.customer_id WITH ROLLUP;"""
                cursor.execute(cmd);
                for i in cursor:
                    print("Customer ID :",i[0])
                    print("Total Amount Spent: Rs",i[1])
                    print()
            #OLAP Query 4
            elif(query_num==3):
                cmd="""SELECT COALESCE(category_id,'All Categories Combined ') AS CategoryID,
                        COUNT(category_id) AS 'Total Number of products in that category',SUM(stock) AS "Total
                        quantity of products in that category"
                        FROM product
                        GROUP BY category_id WITH ROLLUP;"""
                cursor.execute(cmd)
                for i in cursor:
                    print("CategoryID :",i[0])
                    print("Number of Products :",i[1])
                    print("Total Quantity of products in Category :",i[2])
                    print()
            else:
                print("Thank you")
                break
            
        elif(choice==10):
            return
        else:
            print("Sorry you have entered an incorrect option, please eneter the correct option!!") 
        mydb.commit()

def main_admin():
    while(True):
        general_menu_admin()
        admin_id=""
        choice=int(input("Enter your choice :"))
        if(choice==1):
            print("Enter your LogIn Details :")
            email_or_number=input("Phone number or Email Id :")
            password=input("Password :")
            try:
                number=int(email_or_number)
                cmd="""SELECT admin_id 
                        FROM admin A
                        WHERE A.phone_number={0} AND A.password='{1}'""".format(number,password)
                cursor.execute(cmd)
                try:
                    admin_id=cursor.fetchone()[0]
                except:
                    print("You entered Error credentials")
                    exit()
            except ValueError:
                email=email_or_number
                cmd="""SELECT admin_id 
                        FROM admin A
                        WHERE A.email_id='{0}' AND A.password='{1}'""".format(email,password)
                cursor.execute(cmd)
                try:
                    admin_id=cursor.fetchone()[0]
                except:
                    print("You entered Error credentials")
                    exit()
            print(f"\nWelcome, login successful for {admin_id}")
            admin_process(admin_id)
        elif(choice==2):
            print("Enter the following Details to Sign up as the new Admin for the system")
            email_id=input("Email Id :")
            phone_number=int(input("Phone-number :"))
            password=input("Password :")
            special_code=input("Special Code :")
            if(special_code=="iiitd@dbms"):
                cmd="""SELECT COUNT(*) FROM admin;"""
                cursor.execute(cmd)
                number=int(cursor.fetchone()[0])+1
                #dump the data -admin101 not created
                cmd=f""" INSERT INTO Admin(admin_id, email_id, password, phone_number) VALUES('ADMIN{number}','{email_id}','{password}','{phone_number}');"""
                cursor.execute(cmd)
                print("New Admin with ID - ADMIN"+str(number)+" created successfully!!")
                admin_id="ADMIN"+str(number)
                admin_process(admin_id)
            else:
                print("Sorry your special code is incorrect")
        elif(choice==3):
            break; #exit to main menu
        else:
            print("You have entered an incorrect option ! Please choose the correct option")

def browse_wo_signup():
    print("\nChoose option\n1. View all products\n2. Search products by keyword\n3. View products by category\n4.Back to main menu")
    browse_products_choice=int(input())
    if(browse_products_choice==1):
        cmd="SELECT * from Product P;"
        cursor.execute(cmd)
        lst=cursor.fetchall()
        view_products(lst)
        view_a_product(lst,0)
    elif(browse_products_choice==2):
        print("Search bar will display all the item names that has the following search key")
        search_key=input("Enter the item name/key word to be searched :")
        cmd="""CREATE OR REPLACE VIEW Results AS
                SELECT P.name, P.price
                FROM Product P
                WHERE P.name LIKE "%{0}%";""".format(search_key)
        cursor.execute(cmd)
        print("\nA view has been created, it will be displayed now\n")
        cmd="SELECT * FROM onlineretailstore.results;"
        cursor.execute(cmd)
        lst=cursor.fetchall()

        for i in lst:
            print("Name :",i[0])
            print("Price :",i[1])
            print()
        browse_wo_signup()
        # mydb.autocommit=True

#         cmd_create_view="""CREATE OR REPLACE VIEW Results AS
# SELECT P.name, P.price
# FROM Product P
# WHERE P.name LIKE "%{0}%";""".format(search_key)
#         cursor.execute(cmd_create_view)
#         print("A view has been created, it will be displayed now")
#         cmd_display_view="""SELECT * FROM onlineretailstore.results;"""
#         cursor.execute(cmd_display_view)

        # cmd="""SELECT *
        # FROM Product P 
        # WHERE P.name LIKE "%{0}%";""".format(search_key)
        # cursor.execute(cmd)
        # lst=cursor.fetchall()
        # print()
        # view_products(lst)
        # view_a_product(lst,0)
    elif(browse_products_choice==3):
        print("Choose the category")
        cmd="SELECT * FROM category C"
        cursor.execute(cmd)
        lst_cat=cursor.fetchall()
        for i in range(0,len(lst_cat)):
            print(i+1,". ",lst_cat[i][2])
            #print(f"{i+1}. {lst_cat[i][2]}")
        cat_no=int(input("Enter choice: "))
        # cat_no-=1
        cat_id=lst_cat[cat_no -1][0]
        cmd=f"""SELECT *
        FROM Product P 
        WHERE P.category_id = '{cat_id}'"""
        cursor.execute(cmd)
        lst_prod_cat=cursor.fetchall()
        print()
        view_products(lst_prod_cat)
        view_a_product(lst_prod_cat,0)
    # elif(browse_products_choice==4):
    #     browse_wo_signup()
    elif(browse_products_choice==4):
        general_menu()


# loginid 78793 50220
# pwd PtSHC6 V6DkySD

def login_signup():
    print("1. Log in\n2. Sign up\n3. Back")
    login_or_signup_choice=int(input())
    #login code
    if(login_or_signup_choice==1):
        login_id=int(input("Enter the login id :"))
        password=input("Enter the password :").strip()
        # cmd="""SELECT * FROM authentication_credentials
        #     WHERE login_id={0} AND password='{1}';""".format(login_id,password)
        cmd="""SELECT * FROM authentication_credentials
            WHERE login_id={0};""".format(login_id)
        cursor.execute(cmd)
        result=cursor.fetchone()
        if(result[2]==password):
            print("\nLog in successful")
            print(f"Welcome {result[0]}!")
            # global wallet
            # wallet=20000
            main_menu(result[0])
        else:
            print("Authentication failed, incorrect credentials")
            login_signup()
    elif(login_or_signup_choice==2):
        print("Enter details:")
        name1=input("first name: ")
        name2=input("last name: ")
        date=input("birth date in yyyy-mm-dd: ")
        phno=input("phone number: ")
        email=input("email: ")
        house=input("house no.: ")
        street=input("street: ")
        city=input("city: ")
        pincode=input("pincoder: ")
        state=input("state: ")
        country=input("country: ")
        cmd="SELECT * FROM Customer"
        cursor.execute(cmd)
        lst=cursor.fetchall()
        num=len(lst)
        cust_id="CUST"+str(num+1)
        cart_id="CART"+str(num+1)
        points_earned=0
        membership_status="NORMAL"
        # new_cust=[]
        # new_cust.append()
        cmd=f"insert IGNORE into Cart (cart_id, cart_total_amount) values ('{cart_id}', 0);"
        # cmd=f"insert into Cart (cart_total_amount) values (0);"
        cursor.execute(cmd)
        cmd=f"""INSERT IGNORE INTO customer (customer_id, cart_id, first_name, last_name, birth_date, phone_number, email_id, house_number, street, city, pincode, state, country, points_earned, membership_status) 
            values 
            ('{cust_id}', (SELECT cart_id from cart where cart_id='{cart_id}'), '{name1}', '{name2}', '{date}', '{phno}', '{email}', {house}, '{street}', '{city}', {pincode}, '{state}', '{country}', {points_earned}, '{membership_status}');"""
        # cmd=f"insert into Customer (customer_id, cart_id, first_name, last_name, birth_date, phone_number, email_id, house_number, street, city, pincode, state, country, points_earned, membership_status) values ('{cust_id}', '{cart_id}', '{name1}', '{name2}', '{date}', '{phno}', '{email}', {house}, '{street}', '{city}', {pincode}, '{state}', '{country}', {points_earned}, '{membership_status}');"
        cursor.execute(cmd)
        login_id=int(input("enter 5 digit login id:"))
        pwd=input("Enter password as 4 digit number pin: ")
        # auth cred
        cmd=f"insert IGNORE into authentication_credentials (customer_id, login_id, password) values ((SELECT customer_id from customer where customer_id='{cust_id}'),{login_id},'{pwd}');"
        cursor.execute(cmd) #check if pwd repeated
        print("Sign up successful\n")
        login_signup()
    elif(login_or_signup_choice==3):
        general_menu()
    else:
        pass

def view_products(product_list): #displays all products in given list of tuples
    j=0
    for i in product_list:
        print("Product "+str(j+1)+":")
        print("Name : "+i[3])
        print("Description : "+str(i[4]))
        print("Product Price : Rs "+str(i[5]))
        print()
        j+=1

def view_a_product(lst,signed_in,cust_id=None): # equivalent of select product....views detailed summary of one product
    if(not signed_in):
        print("Choose a product to be viewed : ")
        choice=int(input())
        product=lst[choice-1]
        category_id=product[1]
        cursor.execute("SELECT C.category_name FROM category C WHERE C.category_id='{0}'".format(category_id))
        category_name=cursor.fetchone()[0];
        print("\nProduct Details :")
        print("Name :"+product[3])
        print("Category :"+category_name)
        print("Description : "+str(product[4]))
        print("Stock Available : "+str(product[6]))
        print("Price : Rs "+str(product[5]))
        print("\n1. Back\n2. Back to main menu")
        back_choice=int(input())
        if(back_choice==1):
            browse_wo_signup()
        elif(back_choice==2):
            general_menu()
    elif(signed_in):
        print("Choose a product to be viewed : ")
        choice=int(input())
        product=lst[choice-1]
        category_id=product[1]
        cursor.execute("SELECT C.category_name FROM category C WHERE C.category_id='{0}'".format(category_id))
        category_name=cursor.fetchone()[0];
        print("Product Details :")
        print("Name :"+product[3])
        print("Category :"+category_name)
        print("Description : "+str(product[4]))
        print("Stock Available : "+str(product[6]))
        print("Price : Rs "+str(product[5]))
        print("\n1. Add product to cart\n2. Back to main menu")
        back_choice=int(input())
        if(back_choice==2):
            main_menu(cust_id)
        elif(back_choice==1):
            quan=int(input("Enter quantity: "))
            if(quan>product[6]):
                print("not enough stock")
                view_a_product(lst,1,cust_id)
            else:
                cursor.execute(f"SELECT * FROM customer C WHERE C.customer_id='{cust_id}'")
                customer=cursor.fetchone()
                cmd=f"insert into Cart_item (cart_id, product_id, quantity) values ('{customer[1]}', '{product[0]}', {quan});"
                cursor.execute(cmd)
                print("Product added to cart")
                main_menu(cust_id)


def general_menu():
    print("\nChoose option\n1. Browse Products\n2. Log in/Sign up\n3. Exit to Main Menu")
    choice=int(input())
    #browse products section
    if(choice==1):
        browse_wo_signup()
        # print("Choose option\n1. View all products\n2. Search products by keyword\n3. View products by category\n4.Back to main menu")
        # browse_products_choice=int(input())
        # if(browse_products_choice==1):
        #     cmd="SELECT * from Product P;"
        #     cursor.execute(cmd)
        #     lst=cursor.fetchall()
        #     view_products(lst)
        #     view_a_product(lst)
        # elif(browse_products_choice==2):
        #     print("Search bar will display all the item names that has the following search key")
        #     search_key=input("Enter the item name/key word to be searched :")
        #     cmd="""SELECT *
        #     FROM Product P 
        #     WHERE P.name LIKE "%{0}%";""".format(search_key)
        #     cursor.execute(cmd)
        #     lst=cursor.fetchall()
        #     print()
        #     view_products(lst)
        #     view_a_product(lst)
        # elif(browse_products_choice==3):
        #     print("Choose the category")
        #     cmd="SELECT * FROM category C"
        #     cursor.execute(cmd)
        #     lst_cat=cursor.fetchall()
        #     for i in range(0,len(lst_cat)):
        #         print(i+1,". ",lst_cat[i][2])
        #         #print(f"{i+1}. {lst_cat[i][2]}")
        #     cat_no=int(input("Enter choice: "))
        #     # cat_no-=1
        #     cat_id=lst_cat[cat_no -1][0]
        #     cmd=f"""SELECT *
        #     FROM Product P 
        #     WHERE P.category_id = '{cat_id}'"""
        #     cursor.execute(cmd)
        #     lst_prod_cat=cursor.fetchall()
        #     print()
        #     view_products(lst_prod_cat)
        #     view_a_product(lst_prod_cat)
        # elif(browse_products_choice==4):
        #     general_menu()
            
    #login or signup
    elif choice==2:
        login_signup()
    elif choice==3:
        return

def main_menu(cust_id):
    ci=cust_id
    print("\nChoose option:\n1. View all products\n2. Search products by keyword\n3. View products by category\n4. View Cart\n5. Delete cart item\n6. Empty the cart\n7. Check wallet amount\n8. Add money to wallet\n9. Checkout\n10. View order status\n11. Change address\n12. View order history\n13.Log out")
    main_choice=int(input())
    
    if(main_choice==1):
        cmd="SELECT * from Product P;"
        cursor.execute(cmd)
        lst=cursor.fetchall()
        view_products(lst)
        view_a_product(lst,1,cust_id)
    
    elif(main_choice==2):
        print("Search bar will display all the item names that has the following search key")
        search_key=input("Enter the item name/key word to be searched :")
#         cmd_create_view="""CREATE OR REPLACE VIEW Results AS
# SELECT P.name, P.price
# FROM Product P
# WHERE P.name LIKE "%{0}%";""".format(search_key)
#         cursor.execute(cmd_create_view)
#         print("A view has been created, it will be displayed now")
#         cmd_display_view="""SELECT * FROM onlineretailstore.results;"""
#         cursor.execute(cmd_display_view)
        cmd="""SELECT *
        FROM Product P 
        WHERE P.name LIKE "%{0}%";""".format(search_key)
        cursor.execute(cmd)
        lst=cursor.fetchall()
        print()
        view_products(lst)
        view_a_product(lst,1,cust_id)
    
    elif(main_choice==3):
        print("Choose the category")
        cmd="SELECT * FROM category C"
        cursor.execute(cmd)
        lst_cat=cursor.fetchall()
        for i in range(0,len(lst_cat)):
            print(i+1,". ",lst_cat[i][2])
            #print(f"{i+1}. {lst_cat[i][2]}")
        cat_no=int(input("Enter choice: "))
        # cat_no-=1
        cat_id=lst_cat[cat_no -1][0]
        cmd=f"""SELECT *
        FROM Product P 
        WHERE P.category_id = '{cat_id}'"""
        cursor.execute(cmd)
        lst_prod_cat=cursor.fetchall()
        print()
        view_products(lst_prod_cat)
        view_a_product(lst_prod_cat,1,cust_id)
# view cart
    elif(main_choice==4):
        cart_id="CART"+cust_id[4:]
        cmd=f"SELECT * FROM cart_item C WHERE C.cart_id='{cart_id}'"
        cursor.execute(cmd)
        lst=cursor.fetchall()
        if(len(lst)==0):
            print("Cart empty")
            # main_menu()
        else:
            for i in lst:
                quan=i[2]
                flag=0 #repeats not found yet
                for j in lst:
                    if(lst.index(i)!=lst.index(j) and i[1]==j[1]):
                        flag=1
                        quan+=j[2]
                        lst.remove(j)
                # cmd=f"""UPDATE cart_item C SET C.quantity={quan} WHERE C.cart_id= '{i[0]}';"""
                # cursor.execute(cmd)
                new_tuple=(cart_id,i[1],quan)
                lst.append(new_tuple)
                # if flag:
                #     lst.remove(i)
                lst.remove(i)
                
            for i in range(len(lst)):
                print(f"Item{i+1}. " + str(lst[i]))
            # commiting combined cart items
            cmd=f"DELETE FROM cart_item C WHERE C.cart_id='{cart_id}';"
            cursor.execute(cmd)
            # cmd1=f"""ALTER TABLE cart_item DISABLE TRIGGER cart_item_add_and_cart_total_update"""
            # cmd1="""DROP TRIGGER cart_item_add_and_cart_total_amount_update;"""
            # cursor.execute(cmd1)
            for i in range(len(lst)):
                cmd=f"""INSERT INTO cart_item (cart_id, product_id, quantity) VALUES {lst[i]};"""
                cursor.execute(cmd)
            # cmd1=f"""ALTER TABLE cart_item ENABLE TRIGGER cart_item_add_and_cart_total_update"""
            # cursor.execute(cmd1)

            #giving options in view cart page
            cart_choice=int(input("Choose option:\n1. delete a cart item\n2. empty cart\n3. Back\n"))
            if cart_choice==1:
                del_choice=int(input("Enter item no. to delete: "))
                prod_id=lst[del_choice-1][1]
                cmd=f"DELETE FROM cart_item C WHERE C.cart_id='{cart_id}' AND C.product_id='{prod_id}';"
                sure1=int(input("Enter 1 if you are sure to do this else enter 0 to go back: "))
                if sure1:
                    cursor.execute(cmd)
                    print("item deleted")
                elif not sure1:
                    main_menu(cust_id)
            if cart_choice==2:
                sure=int(input("Enter 1 if you are sure to do this else enter 0 to go back: "))
                if sure:
                    cmd=f"DELETE FROM cart_item C WHERE C.cart_id='{cart_id}';"
                    cursor.execute(cmd)
                    cmd=f"""UPDATE cart SET cart.cart_total_amount=0 WHERE cart.cart_id= '{cart_id}';"""
                    cursor.execute(cmd)
                    print("cart emptied\n")
                elif not cart_choice:
                    main_menu(cust_id)
            if cart_choice==3:
                main_menu(cust_id)

#Delete cart item
    elif(main_choice==5):
        cart_id="CART"+cust_id[4:]
        cmd=f"SELECT * FROM cart_item C WHERE C.cart_id='{cart_id}'"
        cursor.execute(cmd)
        lst=cursor.fetchall()
        if(len(lst)==0):
            print("Cart empty\n")
            # main_menu()
        else:
            for i in lst:
                quan=i[2]
                flag=0 #repeats not found yet
                for j in lst:
                    if(lst.index(i)!=lst.index(j) and i[1]==j[1]):
                        flag=1
                        quan+=j[2]
                        lst.remove(j)
                new_tuple=(cart_id,i[1],quan)
                lst.append(new_tuple)
                # if flag:
                #     lst.remove(i)
                lst.remove(i)
            for i in range(len(lst)):
                print(f"Item{i+1}. " + str(lst[i]))
            # commiting combining cart items
            cmd=f"DELETE FROM cart_item C WHERE C.cart_id='{cart_id}';"
            cursor.execute(cmd)
            # cmd1=f"""ALTER TABLE cart_item DISABLE TRIGGER cart_item_add_and_cart_total_update"""
            # cursor.execute(cmd)
            for i in range(len(lst)):
                cmd=f"""INSERT INTO cart_item (cart_id, product_id, quantity) VALUES {lst[i]};"""
                cursor.execute(cmd)
            # cmd1=f"""ALTER TABLE cart_item ENABLE TRIGGER cart_item_add_and_cart_total_update"""
            # cursor.execute(cmd)
        del_choice=int(input("Enter item no. to delete: "))
        prod_id=lst[del_choice-1][1]
        cmd=f"DELETE FROM cart_item C WHERE C.cart_id='{cart_id}' AND C.product_id='{prod_id}';"
        sure2=int(input("Enter 1 if you are sure to do this else enter 0 to go back: "))
        if sure2:
            cursor.execute(cmd)
            print("item deleted\n")
        elif not sure2:
            main_menu(cust_id)

#6. Empty the cart
    elif(main_choice==6):
        cart_id="CART"+cust_id[4:]
        cmd=f"SELECT * FROM cart_item C WHERE C.cart_id='{cart_id}';"
        cursor.execute(cmd)
        lst=cursor.fetchall()
        if(len(lst)==0):
            print("Cart already empty\n")
            # main_menu()
        else:
            sure=int(input("Enter 1 if you are sure to do this else enter 0 to go back"))
            if sure:
                cmd=f"DELETE FROM cart_item C WHERE C.cart_id='{cart_id}';"
                cursor.execute(cmd)
                cmd=f"UPDATE cart SET cart_total_amount=0 WHERE cart_id='{cart_id}'"
                cursor.execute(cmd)
                print("cart emptied\n")

# 7. Check wallet amount
    elif(main_choice==7):
        global wallet
        print(f"Current wallet amount is: {wallet}")
# 8. Add money to wallet
    elif(main_choice==8):
        # global wallet
        print(f"Current wallet amount is: {wallet}")
        amt=int(input("Enter amount to add: "))
        wallet+=amt
        print("Money added\n")
# 9. Checkout
    elif(main_choice==9):
        cart_id="CART"+cust_id[4:]
        print(cart_id)
        print("\nDo you have any coupon to apply?\n1. Yes\n2. No\n")
        coupon_yn=int(input())
        cmd=f"SELECT cart_total_amount FROM cart WHERE cart_id='{cart_id}';"
        cursor.execute(cmd)
        lst_totamt=cursor.fetchone()
        # print(type(lst_totamt))
        totamt=lst_totamt[0]
        print("total amt" ,totamt)
        if coupon_yn==1:
            cpn_code=int(input("Enter the correct coupon code: "))
            cmd=f"SELECT * FROM coupon C WHERE C.coupon_code={cpn_code}"
            cursor.execute(cmd)
            lst_cpn=cursor.fetchall()
            if len(lst_cpn)==0:
                print("Invalid code")
                main_menu(cust_id)
            else:
                discount_pntg=lst_cpn[0][3]
                totamt=totamt*(discount_pntg/100)
                print(f"coupon applied of {discount_pntg}%!!")
        # payment method
        print("\nChoose payment method\n1. wallet\n2. COD\n")
        pm=int(input("choose method number"))
        # print(wallet<totamt)
        # print("wallet",wallet)
        # print(totamt)
        if pm==1 and wallet<totamt:
            print("not enough amount in wallet")
            main_menu(cust_id)
        else:
            print("Im in else")
            # empty cart
            cart_id="CART"+cust_id[4:]
            # print(cart_id)
            cmd=f"SELECT * FROM cart_item C WHERE C.cart_id='{cart_id}';"
            cursor.execute(cmd)
            lst=cursor.fetchall()
            if(len(lst)==0):
                print("Cart already empty")
                # main_menu()
            else:
                #decreasing stock after checkout
                cmd=f"SELECT * FROM cart_item C WHERE C.cart_id='{cart_id}';"
                cursor.execute(cmd)
                lst_del_items=cursor.fetchall()
                for i in lst_del_items:
                    dec_prod_id=i[1]
                    dec_prod_quan=i[2]
                    cmd=f"""UPDATE product
                    SET stock= stock-{dec_prod_quan}
                    WHERE product_id='{dec_prod_id};'"""
                    cursor.execute(cmd)
                    # curr_prod=cursor.fetchone()
                    # # deleting old record
                    # cmd=f"""DELETE FROM product P
                    # WHERE P.product_id='{curr_prod[0]}';"""
                    # cursor.execute(cmd)
                    # # inserting new record
                    # cmd=f"""insert into Product (product_id, category_id, admin_id, name, description, price, stock, discount) 
                    # values 
                    # ('{curr_prod[0]}', '{curr_prod[1]}', '{curr_prod[2]}', '{curr_prod[3]}', '{curr_prod[4]}', {curr_prod[5]}, {curr_prod[6] - dec_prod_quan}, {curr_prod[7]});"""
                    # cursor.execute(cmd)
                # deleting cart items
                cmd=f"DELETE FROM cart_item C WHERE C.cart_id='{cart_id}';"
                cursor.execute(cmd)
                cmd=f"UPDATE cart SET cart_total_amount=0 WHERE cart_id='{cart_id}'"
                cursor.execute(cmd)
                # print("cart emptied")
            # inserting a new order in table
            cmd="SELECT * FROM `Order`;"
            cursor.execute(cmd)
            lst_all_orders=cursor.fetchall()
            order_id="ORDER"+str(len(lst_all_orders)+1)
            tid="TRANS"+str(len(lst_all_orders))
            odate= datetime.today().strftime('%Y-%m-%d')
            sdate=odate
            cmd=f"SELECT * FROM customer WHERE customer_id='{cust_id}'"
            cursor.execute(cmd)
            cust_tuple=cursor.fetchone()
            if pm==1:
                status="Paid"
            else:
                status="Unpaid"
            cmd=f"""insert into Transaction (transaction_id, customer_id, `date-time`, amount, credit_debit_status) values ('{tid}', (SELECT customer_id from customer where customer_id='{cust_id}'), '2016-01-26 22:20:26', 9303, 'Debit');"""
            cursor.execute(cmd)
            cmd=f"""insert into `Order` 
            (order_id, customer_id, coupon_id, transaction_id, shipper_id, order_status, order_date, shipping_date, house_number, street, city, pincode, state, country, tax, delivery_charges, total_amount, net_amount, payment_status)
            values 
            ('{order_id}', '{cust_id}', 'COU054', (SELECT transaction_id from transaction where transaction_id='{tid}'), 'SHIPPER003', 'Processed', '{odate}', '{sdate}', {cust_tuple[7]}, '{cust_tuple[8]}', '{cust_tuple[9]}', {cust_tuple[10]}, null, '{cust_tuple[12]}', 12, 45, {totamt}, {totamt+57}, '{status}') ;"""
            cursor.execute(cmd)
            print("\norder placed\n")

# 10. View order status
    elif(main_choice==10):
        cmd=f"SELECT order_id FROM `Order` O WHERE O.customer_id='{cust_id}'" #all customer orders
        cursor.execute(cmd)
        lst_cust_orders=cursor.fetchall()
        for i in range(len(lst_cust_orders)):
            print(f"{i+1}: {lst_cust_orders[i][0]}\n")
        if(len(lst_cust_orders)==0):
            print("No previous orders")
        else:
            print("Choose order to see status: ")
            order_no=int(input())
            order_id=lst_cust_orders[order_no-1][0]
            cmd=f"SELECT order_status FROM `Order` O WHERE O.order_id='{order_id}'"
            cursor.execute(cmd)
            status=cursor.fetchone()
            print(f"The order status is for order {order_id}: {status[0]}")
            

# 11. Change address
    elif(main_choice==11):
        print("Give new address details: ")
        house_number= input("house number: ")
        street=input("street: ")
        city=input("city: ")
        pincode= input("pincode: ")
        state=input("state: ")
        country=input("country: ")
        cmd=f"""UPDATE customer
        SET house_number='{house_number}', street='{street}', city='{city}', pincode={pincode}, state='{state}', country='{country}'
        WHERE customer_id='{cust_id}';"""
        cursor.execute(cmd)
        print("\nAddress changed successfully!\n")

# 12. View order history
    elif(main_choice==12):
        cmd=f"""CREATE OR REPLACE VIEW OrderHistory AS
        SELECT  order_id, transaction_id, shipper_id, order_status, shipping_date, net_amount, payment_status
        FROM `order` O 
        WHERE O.customer_id = '{cust_id}';"""
        cursor.execute(cmd)
        print("View has been created\n")

        cmd=f"""SELECT  order_id, transaction_id, shipper_id, order_status, shipping_date, net_amount, payment_status
        FROM `order` O WHERE O.customer_id = '{cust_id}'"""
        cursor.execute(cmd)
        lst_orders=cursor.fetchall()
        for i in range(len(lst_orders)):
            print(f"order{i+1}: {lst_orders[i]}")
        if len(lst_orders)==0:
            print("No past orders")
#13.Log out 
    elif(main_choice==13):
        print("Logged out\n")
        general_menu()
    main_menu(cust_id)

def retailstore():
    print("\n\n"+""*20 + " Welcome to OnlineRetailStore "+""*20+"\n\n" )

    grant1="""GRANT ALL PRIVILEGES ON *.* TO 'root1'@'localhost' WITH GRANT OPTION;"""
    cursor.execute(grant1)
    grant2="""GRANT ALL PRIVILEGES ON *.* TO 'admin_dbms'@'localhost' WITH GRANT OPTION;"""
    cursor.execute(grant2)
    print("Grants given: ")

    print("Choose\n1. Enter as Customer\n2. Enter as Admin\n3. Exit Application")
    ans=int(input())
    if ans==1:
        general_menu()
        retailstore()
    elif ans==2:
        main_admin()
        retailstore()
    elif ans==3:
        print("Thanks for visiting!")
#without sign in-----------------------------------------------------------------------------------------
# print("\n\n"+""*20 + " Welcome to OnlineRetailStore "+""*20+"\n\n" )
# print("Choose\n1. Enter as Customer\n2. Enter as Admin\n")
# ans=int(input())
# if ans==1:
#     general_menu()
# elif ans==2:
#     main_admin()

retailstore()

    
    
    


# print("""Choose the query to be performed:""")
# print("""1.login and view order history \n2.search product catalogue by key word\n""")
# query_num=int(input())

# #Embedded Query 1
# if(query_num==1):

#     login_id=int(input("Enter the login id :"))
#     password=input("Enter the password :").strip()
#     cmd="""SELECT * FROM authentication_credentials
#         WHERE login_id={0} AND password='{1}';""".format(login_id,password)

#     cursor.execute(cmd)
#     result=cursor.fetchone()
#     customer_id=result[0]
#     print(customer_id)
#     cmd="""SELECT * FROM `order`
#         WHERE customer_id='{0}'""".format(customer_id)
#     cursor.execute(cmd)
#     all_order_id=[]
#     for i in cursor:
#         all_order_id.append(i[0])
#     print("""Which Order do you want to see the order history for?""")
#     num=1
#     for i in all_order_id:
#         print(num," = ",i)
#         num+=1
#     choice=int(input("Enter your choice : "))
#     order_id=all_order_id[choice-1]

#     cmd="""SELECT OI.*, O.order_date, O.order_status
#     FROM Order_item OI, `Order` O
#     WHERE OI.order_id = O.order_id AND O.order_id='{0}';
#     """.format(order_id)
#     cursor.execute(cmd)
#     for i in cursor:
#         print(i)


# #Embedded Query 2
# elif(query_num==2):
#     print("Search bar will display all the item names that has the following search key")
#     search_key=input("Enter the item name/key word to be searched :")
#     cmd="""SELECT P.name, P.description, P.price
#     FROM Product P 
#     WHERE P.name LIKE "%{0}%";""".format(search_key)
#     cursor.execute(cmd)
#     for i in cursor:
#         print(i