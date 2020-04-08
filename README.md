# Django-Bookstore

Bookstore 
This is an e-commerce website for a fictional company named Bookstore that sells books.

The company is managed by 3 categories of members:
1. Owners
2. Office Employees
3. Dispatcher

I created 3 different groups for each type of members and designed 3 admin pages with their own permissions. For example:
Owners have full access(equivalent to superusers), Office Employees manage the products and have access to orders and the Dispatchers will manage the orders(and only view the products).

Regular users will navigate to Products tab where they will find a list of available(in stock) books and click on the desired one to open the detail view. From there, if the book is desired, you can add it to the basket and continue your shopping.

Once you're done shopping, you can open the basket and adjust your desired quantities, delete items or make modifications if needed and place the order.

If the user is not authenticated, he/she will be redirected to the login/signup page. If the user doesn't have an account, he/she will create one and it will require an email verification in order to log in(I used SendGrid as SMTP).

Once the user verified his/her email, he/she can continue with the order and complete the billing/shipping address form.

Every user has a designed page where they can view all their submitted orders. If they have any question regarding any order they've made, there is a link to enter live chat room with one of the employees.
Next, the employees are notified that someone opened a chat room(In this case, I used a basic Server Sent Event) and provided specific link to enter the room.
For this feature, I used Django Channels 2.0. I made two basic classes in my consumers.py file:
1. Chat Room
2. Chat Notify

I used AsyncJsonWebSocketConsumer for my Chat Room and wrote a few coroutines in order to Connect, Disconnect, Send/Receive Json. I also configured Redis for this feature.
For the more "experienced" Employees who want to do their job in a more "developer" way, I implemented an API for them.

They can see and/or manage the orders, products and user details(addresses). They can change statuses from "New" to "Processing" and they can add new products or edit the current ones.

For this feature I used Django Rest Framework. I mostly used HyperinkedModelSerializer for Serializers and ModelViewSet as viewsets in order to get all the CRUD operations.
