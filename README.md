# Online-Retail-Store

This project utilises all the fundamental learnings of my DBMS course. Using various concepts, we have tried our best to create a robust backend database.
Guide : Vikram Goyal and Mukesh Mohania

# Scope
Our Project focuses on creating a backend database for an online retail store. The main objective of this
project is to develop an online retail store with a robust end-to-end database application as the
primary part of the back-end, which allows customers to navigate through the product catalog
and purchase products. Like standard retail stores like BigBazar, Amazon, and Flipkart, we will
sell customers products of different categories, such as electronics, groceries, etc, and offer
them the best deals according to their requirements. They can find the products according to
their needs, like products belonging to some Company, products that fall in some price range,
etc, and make payments. There will be a similar setup for employees where their data will be
stored if time permits. Different payment methods will be linked. In terms of data, we will be
storing customer information, their personal information, phone number, email address and
address, both office, temporary and residential, their previous deals, returns and orders, and
rewards and coupons available. Data regarding products will be stored like description, price,
reviews, and ratings, shipping/transportation details, discounts available.

# Constraints
1. A customer(identified with email-id or mobile no.) can have only one account in the store
application.
2. One account can have only a single cart.
3. One account can have multiple payment methods saved in the account, so this is a
one-to-many relationship.
4. The relationship between customers and products will be many-to-many as multiple
customers can buy the same products and also one customer can buy multiple products.
5. There can be multiple sellers for the same product, while a single seller can also sell
multiple products so again this would be a many-to-many relationship.
6. The order should be placed only after payment is confirmed. The cart should be emptied
once order is placed.

## Functional Requirements:
# From Customer’s side
1. Customer Login/SignUp: This feature will help the customer to log in or sign up if he is
new to the platform
2. Search the Products: This feature helps the customer search the product
3. View the Product: This feature helps the customer view the product and displays its
description and features
4. Add to the Cart: This feature adds the product to the user’s cart and keeps track of all
the products that were added to the cart
5. View Cart: Go to cart to check the added products or remove any.
6. Buy the Cart: This feature helps the user buy the entire cart and place the order.
7. Payment Methods: This feature helps the customer choose from one payment option,
whether it is COD, UPI, Net Banking, Debit Card, etc
8. Track the Order: This feature helps the customer get the current status of the order
where it is right now.
9. Best Sellers: This feature will feature the most frequently sold products
10. Deals: This feature will showcase deals according to special occasions.

    
# From Admin’s side
1. Enter as Admin
2. Add Category
3. Delete Category
4. Add Product
5. Delete Product
6. Set Discount on Products
7. Add deals
8. Update details on products
9. Sales analysis

I had made this project with the help of Siddharth Gupta, my DMBS project partner.
