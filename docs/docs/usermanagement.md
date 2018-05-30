# User Management and Accounting

In general, the openEO API only defines a minimum subset of user management and accounting functionality. It allows to

* [authenticate and authorize](http://www.differencebetween.net/technology/difference-between-authentication-and-authorization/) a user
* query the credit a user has available
* estimate costs for certain operations
* get information about produced costs
* limit costs of certain operations

Therefore, the API leaves some aspects open that have to be handled by the back-ends separately, including 

* user registration
* credential recovery, e.g. retrieving a forgotten password
* user data management, e.g. changing the users payment details or email address
* payments, i.e. topping up credits for pre-paid services or paying for post-paid services
* other accounting related tasks, e.g. creating invoices.

