import mysql.connector
mydb=mysql.connector.connect(
    host='127.0.0.1',
    database="onlineretailstore",
    user='root',
    password='tony022002@Kuku'
)
cursor=mydb.cursor()

while(True):
    #Menu
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
            print("Number of qunatities :",i[1]);
            print("Total Cost of this Category : Rs",i[2])
    
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