import mysql.connector
from datetime import datetime
from datetime import datetime, date, timedelta

mydb=mysql.connector.connect(
    host='127.0.0.1',
    database="onlineretailstore",
    user='root',
    password='root'
)

wallet = 20000
cursor=mydb.cursor()
# mydb.get_autocommit()
mydb.autocommit=True
# mydb.get_autocommit()

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
        cmd="""SELECT *
        FROM Product P 
        WHERE P.name LIKE "%{0}%";""".format(search_key)
        cursor.execute(cmd)
        lst=cursor.fetchall()
        print()
        view_products(lst)
        view_a_product(lst,0)
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
            print("Log in successful")
            print(f"Welcome {result[0]}!")
            # global wallet
            # wallet=20000
            main_menu(result[0])
        else:
            print("authentication failed, incorrect credentials")
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
        print("Product Details :")
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
    print("\nChoose option\n1. Browse Products\n2. Log in/Sign up")
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
            # for i in range(len(lst)):
            #     for j in range(len(lst)):
            #         if(i!=j and lst[i][1]==lst[j][1]): ##same product id
            #             new_tuple=(cart_id,lst[i][1],lst[i][2]+lst[j][2])
            #             # lst[i][2]+=lst[j][2]
            #             lst[i]=new_tuple
            #             lst.remove(lst[j]) #combining duplicate products into one cart item for viewing
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
            for i in range(len(lst)):
                cmd=f"""INSERT INTO cart_item (cart_id, product_id, quantity) VALUES {lst[i]};"""
                cursor.execute(cmd)
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
            for i in range(len(lst)):
                cmd=f"""INSERT INTO cart_item (cart_id, product_id, quantity) VALUES {lst[i]};"""
                cursor.execute(cmd)
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
        print(wallet<totamt)
        print("wallet",wallet)
        print(totamt)
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
        cmd=f"""SELECT  order_id, transaction_id, shipper_id, order_status, shipping_date, net_amount, payment_status
        FROM `order` O WHERE O.customer_id = '{cust_id}'"""
        cursor.execute(cmd)
        lst_orders=cursor.fetchall()
        for i in range(len(lst_orders)):
            print(f"order{i+1}: {lst_orders[i]}")
#13.Log out 
    elif(main_choice==13):
        print("Logged out\n")
        general_menu()
    main_menu(cust_id)
    
#without sign in-----------------------------------------------------------------------------------------
print("\n\n"+""*20 + " Welcome to OnlineRetailStore "+""*20+"\n\n" )
general_menu()

    
    
    


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