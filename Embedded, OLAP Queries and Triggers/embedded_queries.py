import mysql.connector
mydb=mysql.connector.connect(
    host='127.0.0.1',
    database="onlineretailstore",
    user='root',
    password='tony022002@Kuku'
)
cursor=mydb.cursor()

print("""Choose the query to be performed:""")
print("""1.login and view order history \n2.search product catalogue by key word\n""")
query_num=int(input())

#Embedded Query 1
if(query_num==1):

    login_id=int(input("Enter the login id :"))
    password=input("Enter the password :").strip()
    cmd="""SELECT * FROM authentication_credentials
        WHERE login_id={0} AND password='{1}';""".format(login_id,password)

    cursor.execute(cmd)
    result=cursor.fetchone()
    customer_id=result[0]
    print(customer_id)
    cmd="""SELECT * FROM `order`
        WHERE customer_id='{0}'""".format(customer_id)
    cursor.execute(cmd)
    all_order_id=[]
    for i in cursor:
        all_order_id.append(i[0])
    print("""Which Order do you want to see the order history for?""")
    num=1
    for i in all_order_id:
        print(num," = ",i)
        num+=1
    choice=int(input("Enter your choice : "))
    order_id=all_order_id[choice-1]

    cmd="""SELECT OI.*, O.order_date, O.order_status
    FROM Order_item OI, `Order` O
    WHERE OI.order_id = O.order_id AND O.order_id='{0}';
    """.format(order_id)
    cursor.execute(cmd)
    for i in cursor:
        print(i)


#Embedded Query 2
elif(query_num==2):
    print("Search bar will display all the item names that has the following search key")
    search_key=input("Enter the item name/key word to be searched :")
    cmd="""SELECT P.name, P.description, P.price
    FROM Product P 
    WHERE P.name LIKE "%{0}%";""".format(search_key)
    cursor.execute(cmd)
    for i in cursor:
        print(i)