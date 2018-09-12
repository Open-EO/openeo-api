# User Management and Accounting

In general, the openEO API only defines a minimum subset of user management and accounting functionality. It allows to

* [authenticate and authorize](http://www.differencebetween.net/technology/difference-between-authentication-and-authorization/) a user, which may include [user registration with OpenID Connect](http://openid.net/specs/openid-connect-registration-1_0.html),
* handle storage space limits (disk quota),
* manage billing, which includes to
    * query the credit a user has available,
    * estimate costs for certain operations (data processing and downloading),
    * get information about produced costs,
    * limit costs of certain operations.

Therefore, the API leaves some aspects open that have to be handled by the back-ends separately, including 

* credential recovery, e.g. retrieving a forgotten password
* user data management, e.g. changing the users payment details or email address
* payments, i.e. topping up credits for pre-paid services or paying for post-paid services
* other accounting related tasks, e.g. creating invoices,
* user registration (only specified when OpenID Connect is implemented).

