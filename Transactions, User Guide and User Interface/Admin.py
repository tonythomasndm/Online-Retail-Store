import mysql.connector
mydb=mysql.connector.connect(
    host='127.0.0.1',
    database="onlineretailstore",
    user='root',
    password='tony022002@Kuku'
)
mydb.autocommit=True
cursor=mydb.cursor()

def general_menu_admin():
    print("Choose the way to enter as an admin : \n1. LogIn as Admin\n2. Sign Up as a new Admin\n3. Exit to Main Menu")
def admin_process(admin_id):
    while(True):
        print("Menu :\n1.Add a category\n2.Delete a category\n3.Add a product\n4.Delete a product\n5.Set discount on a product\n6.Change category of a product\n7.Update details on a category\n8.Update details on a product\n9.Sales Analysis\n10.Back to Previous menu\n")
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
            
        elif(choice==10):
            return
        else:
            print("Sorry you have entered an incorrect option, please eneter the correct option!!") 
        mydb.commit()
            
if __name__=='__main__':
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
            break;#exit to main menu
        else:
            print("You have entered an incorrect option ! Please choose the correct option")