# The InkShop 
##### An E-Commerce Site by MllrB
##### Developed for CodeInstute Milestone Project 4 - Full Stack Development with Django
--------
# Testing Documentation
- [Interesting Bugs](#Interesting-Bugs)
- [Navbar Links](#Navbar-Links)
    - [Desktop + Laptop Devices](#Desktop-+-Laptop-Devices)
    - [Mobile Devices](#Mobile-Devices)
- [Footer Links](#Footer-Links)
- [Account Login/Logout Flow](#Account-Login/Logout-Flow)
- [User Profile](#User-Profile)
    - [Billing Details](#Billing-Details)
    - [Delivery Addresses](#Delivery-Addresses)
    - [Favourited Products](#Favourited-Products)
    - [Order History](#Order-History)
    - [Edit Recipe Bugs](#Edit-Recipe-Bugs)
- [Product Maintenance](#Product-Maintenance)
- [Content management](#Content-management)
- [Basket](#Basket)
- [Checkout](#Checkout)
    - [Confirming an order with an anonymous user](#Confirming-an-order-with-an-anonymous-user)
    - [Confirming an order with an authorised user](#Confirming-an-order-with-an-authorised-user)

## Interesting Bugs
I have come across some difficult bugs during the development of this project and the following testing highlighted a few more for me.

Of particular interest is a bug concerning the shopping basket. When I initially designed the shopping basket I had two quite different layouts in mind for desktop and mobile devices so when constructing them, rather than trying to configure them in one block of code, I separated them out into two blocks within the one page. One for desktop, one for mobile. Both were using the same resources, however, and although this didn't cause much of a problem for the most part, when it came to the quantity select script, it did. The quantity select buttons were not behaving as expected and that was because there were two instances of the same ID for each product, one for mobile and one for desktop. Strapped for time, I settled for a quick solution. I put the code for the mobile views in a new html file and into the basket app's includes folder. This page is then included in a div that is only displayed on screens narrower than 768px. This solution works, however, when resizing a desktop window to narrower than 768px, it becomes necessary to refresh the page to see the basket. 

In the [testing below](#Confirming-an-order-with-an-authorised-user) I have described a bug that I have since at least partially fixed regarding the checkout process for authenticated users. It occurred when a user completed an order without entering a delivery address. The bug was occurring because a blank address reference was being passed to the session and used in the checkout view to to get the correct DeliveryAddress instance and attach it to the order. I have since included a condition that if the delivery address reference is blank, to set the order details to the user's billing address. I am confident that this works if the order is completed in the view. I'm not as confident that the order will complete correctly if completed in the Stripe webhook handler.

I also encountered a very strange bug with the layout of certain products. For some products, product list layout was displaying with the pricing, quantity selector and add to basket being pushed to the bottom left of the product card. It took a while, but i found out that the issue was being caused by some hidden html in the product description. I was using the truncatewords and safe django template filters and a combination of both was causing the bug. I switched to using a combination of the truncatewords_html and safe template filters and this fixed the layout problem.

## Navbar Links
##### Desktop + Laptop Devices
1. Test: Clicking the logo.
    * Method: 
        - Navigate away from the homepage and click the logo
    * Expected result: 
        - The user should be returned to the homepage from any other page on the website.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/`
    * Result:
        - Clicking the logo returns the user to the homepage
        - URL: `https://ci-ms4-inkshop.herokuapp.com/`

2. Test: Clicking the "Browse" icon.
    * Method: 
        - From all pages on the website, click the 'Browse Recipes' link 
    * Expected result: 
        - A dropdown menu containing 3 options; Supplies; Printers; Accessories; should appear.
    * Result:
        - A dropdown menu containing 3 options; Supplies; Printers; Accessories; appears.

3. Test: Selecting the options from the Browse icon
    1. Supplies
        * Method: 
            - Click 'Browse' and click 'Supplies' 
        * Expected result: 
            - The user should be directed to a page showing the categories with the relevant_model field of 'supplies'.
            - URL: `https://ci-ms4-inkshop.herokuapp.com/category/supplies`
        * Result:
            - The user is shown the relevant category page
            - URL: `https://ci-ms4-inkshop.herokuapp.com/category/supplies`
    2. Printers
        * Method: 
            - Click 'Browse' and click 'Printers' 
        * Expected result: 
            - The user should be directed to a page showing the categories with the relevant_model field of 'printers'.
            - URL: `https://ci-ms4-inkshop.herokuapp.com/category/printers`
        * Result:
            - The user is shown the relevant category page
            - URL: `https://ci-ms4-inkshop.herokuapp.com/category/printers`
    3. Accessories
        * Method: 
            - Click 'Browse' and click 'Accessories' 
        * Expected result: 
            - The user should be directed to a page showing the categories with the relevant_model field of 'Accessories'.
            - URL: `https://ci-ms4-inkshop.herokuapp.com/category/accessories`
        * Result:
            - The user is shown the relevant category page
            - URL: `https://ci-ms4-inkshop.herokuapp.com/category/accessories`
    
4. Test: Clicking the "Account" icon.
    1. User not authenticated
        * Method: 
            - From all pages on the website, click the 'Account' icon with user not logged in
        * Expected result: 
            - A dropdown menu containing 1 option, Log In/Register, should appear.
        * Result:
            - A dropdown menu containing 1 option, Log In/Register, appears.
    2. Authenticated User but not superuser logged in
        * Method: 
            - From all pages on the website, click the 'Account' icon with user logged in
        * Expected result: 
            - A dropdown menu containing 2 options, Profile and Log Out, should appear.
        * Result:
            - A dropdown menu containing 2 options, Profile and Log Out, appears.
    3. Authenticated Super User
        * Method: 
            - From all pages on the website, click the 'Account' icon with super user logged in
        * Expected result: 
            - A dropdown menu containing 4 options, Content Management, Product Maintenance, Profile and Log Out, should appear.
        * Result:
            - A dropdown menu containing 4 options, Content Management, Product Maintenance, Profile and Log Out, appears.

5. Test: User not Authenticated clicks Log In/Register.
    * Method: 
        - Unauthenticated User clicks Account follwed by Log In/Register 
    * Expected result: 
        - The user should be directed to the account login page which includes both log in and register options.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/account/`
    * Result:
        - User directed to the account login page including both log in and register options
        - URL: `https://ci-ms4-inkshop.herokuapp.com/account/`

6. Test: Authenticated User clicks Log Out.
    * Method: 
        - Authenticated User clicks Account followed by Log Out
    * Expected result: 
        - The user should be directed to the account logout page.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/accounts/logout/`
    * Result:
        - User directed to the account logout page.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/accounts/logout/`
7. Test: Authenticated User (including super user)clicks Profile.
    * Method: 
        - Authenticated User clicks Account followed by Profile.
    * Expected result: 
        - The user should be directed to the user profile page.
        - The profile page should be defaulted to show the user's billing information.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/customers/billing/`
    * Result:
        - User directed to the user profile page.
        - The profile page shows the user's billing information
        - URL: `https://ci-ms4-inkshop.herokuapp.com/customers/billing/`

8. Test: Authenticated Super User clicks Product Maintenance.
    * Method: 
        - Authenticated Super User clicks Account followed by Product Maintenance.
    * Expected result: 
        - The user should be directed to the product maintenance page.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/product_maintenance/`
    * Result:
        - User directed to the product maintenance page.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/product_maintenance/`

9. Test: Authenticated Super User clicks Content Management.
    * Method: 
        - Authenticated Super User clicks Account followed by Content Management.
    * Expected result: 
        - The user should be directed to the content management page.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/content_management/`
    * Result:
        - User directed to the content management page.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/content_management/`

10. Test: Any user Clicks on the Basket icon.
    * Method: 
        - User clicks on the basket icon with nothing in the basket.
        - User clicks on the basket icon with something in the basket.
        - User hovers on the basket icon with nothing in the basket.
        - User hovers on the basket icon with something in the basket.
    * Expected result: 
        - Empty Basket: The user should be directed to the basket page and prompted that they do not have anything in the basket.
        - Basket with Items: The user should be directed to the basket page and shown their basket items.
        - Empty Basket Hover: A toast should appear below the basket advising that there is nothing in the basket.
        - Basket with Items Hover: A toast should appear showing the basket items.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/basket/`
    * Result:
        - Empty Basket: User directed to the basket page and prompted that there is nothing in the basket.
        - Basket with Items: User is directed to the basket page and shown their basket items.
        - Empty Basket Hover: A toast appears below the basket advising that there is nothing in the basket.
        - Basket with Items Hover: A toast appears showing the basket items.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/basket/`


11. Test: Any User enters a search term and clicks search/presses enter.
    * Method: 
        - Any User enters search term 'HP 304' and clicks search/presses enter.
        - Any User enters search term 'HP304' and clicks search/presses enter.
    * Expected result: 
        - Search Term - HP 304: The user should be directed to a product list page showing 4 results.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/?q=hp+304`
        - Search Term - HP304: The user should be directed to a product page showing no results.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/?q=hp304`
    * Result:
        - Search Term - HP 304: The user should be directed to a product list page showing 4 results.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/?q=hp+304`
        - Search Term - HP304: The user should be directed to a product page showing no results.
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/?q=hp304`

    _Note: Although the search term without spaces returns the result I expected, ideal behaviour would be to return the same result as the search term with spaces._

[back to top](#Testing-Documentation)
------------
#### Mobile Devices
12. Test: Repeat tests 4 through 11 above from the side navigation panel on a mobile device.
    * Expected result: 
        - Identical behaviour as for tests 2 through 5 above.
    * Result:
        - Identical behaviour as for tests 2 through 5 above.

    _Note: Test 4 indicated that for a superuser, the dropdown menu items content management and product maintenance did not fit on the page. The fix was to add a class to the mobile navigation dropdown div to reposition the dropdown to the left._

13. Test: Click the menu 'burger' button.
    * Method: 
        - Press the menu button.
        - Press the 'home' menu item
        - Press the 'Supplies' menu item
        - Press the 'Printers' menu item
        - Press the 'Accessories' menu item
        - Press any sub menu item
    * Expected result: 
        - Menu: Dropdown containing 4 items appears, Home, Supplies, Printers and Accessories.
        - Home: Directs the user to the home page
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products`
        - Supplies: Opens a sub-menu containing categories to navigate to.
        - Printers: Opens a sub-menu containing categories to navigate to.
        - Accessories: Opens a sub-menu containing categories to navigate to.
        - Sub Menu Item: Redirects user to a product list page containing products from the selected category
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/by_category/'category number'`
    * Result:
        - Menu: Dropdown containing 4 items appears, Home, Supplies, Printers and Accessories.
        - Home: User directed to the home page
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products`
        - Supplies: Opens a sub-menu containing categories to navigate to.
        - Printers: Opens a sub-menu containing categories to navigate to.
        - Accessories: Opens a sub-menu containing categories to navigate to.
        - Sub Menu Item: Redirects user to a product list page containing products from the selected category. Chosen example - Supplies > Printer Kits
        - URL: `https://ci-ms4-inkshop.herokuapp.com/products/by_category/978/`

[back to top](#Testing-Documentation)

### Footer Links
1. Test: Click Products links.
    * Method:
        - Click Inks/Toners
        - Click Printers
        - Click Printing Paper
        - Click Blank Media & Storage
    * Expected result:
        - Inks/Toners: Redirect User to Supplies category page. URL: `https://ci-ms4-inkshop.herokuapp.com/category/supplies`
        - Printers: Redirect User to Printers category page. URL: `https://ci-ms4-inkshop.herokuapp.com/category/printers`
        - Printing Paper: Redirect User to products_by_category page. URL: `https://ci-ms4-inkshop.herokuapp.com/products/by_category/714/`
        - Blank Media & Storage: Redirect User to products_by_category page. URL: `https://ci-ms4-inkshop.herokuapp.com/products/by_category/1554/`
    * Result:
        - Inks/Toners: Redirected to expected URL
        - Printers: Redirected to expected URL
        - Printing Paper: Redirected to expected URL
        - Blank Media & Storage: Redirected to expected URL

2. Test: Click About links.
    * Method:
        - Click About the Inkshop
        - Click Delivery Info
        - Click FAQs
        - Click Terms & Conditions
        - Click Privacy Policy
    * Expected result:
        - About the InkShop: Redirect User to About Us content page. URL: `https://ci-ms4-inkshop.herokuapp.com/about/`
        - Delivery Info: Redirect User to About Us content page. URL: `https://ci-ms4-inkshop.herokuapp.com/delivery_info/`
        - FAQs: Redirect User to About Us content page. URL: `https://ci-ms4-inkshop.herokuapp.com/faqs/`
        - Terms & Conditions: Redirect User to About Us content page. URL: `https://ci-ms4-inkshop.herokuapp.com/terms_and_conditions/`
        - Privacy Policy: Redirect User to About Us content page. URL: `https://ci-ms4-inkshop.herokuapp.com/privacy_policy/`
    * Result:
        - About the InkShop: Redirected to expected URL
        - Delivery Info: Redirected to expected URL
        - FAQs: Redirected to expected URL
        - Terms & Conditions: Redirected to expected URL
        - Privacy Policy: Redirected to expected URL
    
3. Test: Click Email link.
    * Method:
        - Click Email: info@mllrb.com
    * Expected result:
        - Open email Client
    * Result:
        - Opens email client

[back to top](#Testing-Documentation)

## Account Login/Logout Flow

1. Test: Register for account
    - Method: 
        1. Unauthenticated user registers for an account with email and password
        2. Unauthenticated user verifies email address 
        3. Authenticated User tries to register for account
    - Expected Results:
        1. User is redirected to an advisory page prompting the user that a verification url has been emailed to them.
        1. Toast appears advising user that an email verification URL has been sent to their email address.
        2. User is redirected to their profile page upon verification of email address.
        3. Authenticated user advised that they already have an account
    - Results:
        1. User is redirected to an advisory page prompting the user that a verification url has been emailed to them.
        1. Toast appears advising user that an email verification URL has been sent to their email address.
        2. User is redirected to their profile page upon verification of email address.
        3. Authenticated user advised that they already have an account however user is redirected to unstyled signup page.

2. Test: Sign into account with email and password
    - Method: 
        - Unauthenticated user signs into account with email and password
    - Expected Results:
        - User is logged in and redirected to their user profile page.
    - Results:
        - User is logged in and redirected to their user profile page.

3. Test: Sign into account using sign in with Google
    - Method: 
        - Unauthenticated user signs into account via sign in with google
    - Expected Results:
        - User is redirected to gmail account selection page
        - Upon log in, user is redirected to their profile page
        - The user's profile page has their avater, email address and full name pre-populated
    - Results:
        - User is redirected to gmail account selection page
        - Upon log in, user is redirected to their profile page
        - The user's profile page has their avater, email address and full name pre-populated

    _I attempted this test with three separate gmail accounts. 2 succeeded and one failed. I think this is due to my post_save reciever for SocialAccount logins. Upon save I attempt to create a user with the name to the left of the @ in the users email address set to the User username I think that this is causing a conflict if the same username already exists and was returning a server 500 error. I have attempted to rectify this error with some extra logic in the post_save receiver and it appears to have worked, however, requires further testing_

4. Test: Log Out with any User
    - Method: 
        - Log out with any user
    - Expected Results:
        - User is redirected to sign out confirmation page, URL: `https://ci-ms4-inkshop.herokuapp.com/accounts/logout/`
        - Upon signout confirmation, the user is redirected to the homepage, URL: `https://ci-ms4-inkshop.herokuapp.com/` 
    - Results:
        - User is redirected to sign out confirmation page, URL: `https://ci-ms4-inkshop.herokuapp.com/accounts/logout/`
        - Upon signout confirmation, the user is redirected to the homepage, URL: `https://ci-ms4-inkshop.herokuapp.com/` 


[back to top](#Testing-Documentation)


## User Profile
### Billing Details
1. Test: Updating billing address details is persistent
    - Method: After each test, update the user details using the update info button
        1. Change/Delete Full Name
        2. Enter/Change/Delete Phone Number
        3. Enter/Change/Delete Address Line 1
        4. Enter/Change/Delete Address Line 2
        5. Enter/Change/Delete Town/City
        5. Enter/Change/Delete County
        7. Enter/Change/Delete Postcode/Eircode
        8. Enter/Change/Unselected Country
        9. Upload Avatar image
        10. Clear Avatar image
    - Expected Results:
        1. On Change and update, the user's full name is changed. On delete the field is left empty.
        2. On Change and update, the user's phone number is changed. On delete the form should not submit.
        3. On Change and update, the user's address line is changed. On delete the field is left empty.
        4. On Change and update, the user's address line is changed. On delete the field is left empty.
        5. On Change and update, the user's town/city is changed. On delete the field is left empty.
        5. On Change and update, the user's county is changed. On delete the field is left empty.
        7. On Change and update, the user's postcode/eircode is changed. On delete the field is left empty.
        8. On Change and update, the user's country is changed. If unselected the form should not submit.
        9. On upload, the user's profile image changes.
        10. On Clear the user's profile image reverts to image url or defaut image.
    - Results:
        1. On Change and update, the user's full name is changed. On delete the field is left empty.
        2. On Change and update, the user's phone number is changed. On delete the form does not submit.
        3. On Change and update, the user's address line is changed. On delete the field is left empty.
        4. On Change and update, the user's address line is changed. On delete the field is left empty.
        5. On Change and update, the user's town/city is changed. On delete the field is left empty.
        5. On Change and update, the user's county is changed. On delete the field is left empty.
        7. On Change and update, the user's postcode/eircode is changed. On delete the field is left empty.
        8. On Change and update, the user's country is changed. If unselected the form does not submit.
        9. PASSES if user does not have a profile_pic_src url, FAILS: if user has a profile_pic_src url.
            - Fix: Changed the order of the conditions for which to display the users profile_pic_src and profile_pic to favour the profile_pic first.
        10. On Clear the user's profile image reverts to profile_pic_url or defaut image. Attempted on fix of test 9 and is working.

[back to top](#Testing-Documentation)

### Delivery Addresses
1. Test: Adding a delivery address
    - Method: 
        1. Click the add delivery address button and fill in the form
        2. Try to add another delivery address with the same address ref as entered in 1.
    - Expected Results:
        1. The user's delivery details are saved and the user is returned to the delivery addresses menu. The address reference is now displayed in a list and upon clicking those particular address details are shown in a prepopulated form.
        2. The user is prompted that they must use a unique address reference
    - Results:
        1. The user's delivery details are saved and the user is returned to the delivery addresses menu. The address reference is now displayed in a list and upon clicking those particular address details are shown in a prepopulated form.
        2. End Result passes, behavious fails. The user is prevented from adding a new address with the same reference, however, a generic error message is shown rather than the desired form error telling the user that they must have a unique address reference. I will revisit this as I had the form validation error showing but it was causing a validation error when updating an existing address. 

2. Test: Adding a delivery address
    - Method: 
        - Click on an existing address and upadte the details within.
    - Expected Results:
        - The user is shown their existing delivery address details and any updated details are saved.
    - Results:
        - The user is shown their existing delivery address details and any updated details are saved.


3. Test: Remove a delivery address
    - Method: 
        - Click the delete button for any delivery address.
    - Expected Results:
        - The delivery address is no longer available to the user
    - Results:
        - The delivery address is no longer available to the user

[back to top](#Testing-Documentation)

### Favourited Products
1. Test: Add a product to favourites from product list page.
    - Method: 
        - Add a product to favourites from product list page and check that is appears in the user's favourite products
    - Expected Results:
        - The user is shown a toast confirming that the product has been added to their favourites the product is now listed in their favourites
    - Results:
        - The user is shown a toast confirming that the product has been added to their favourites the product is now listed in their favourites.

2. Test: Add a product to favourites from product detail page
    - Method: 
        - Add a product to favourites from product detail page and check that is appears in the user's favourite products
    - Expected Results:
        - The user is shown a toast confirming that the product has been added to their favourites the product is now listed in their favourites
    - Results:
        - The user is shown a toast confirming that the product has been added to their favourites the product is now listed in their favourites.

3. Test: Remove a product from favourites from profile page.
    - Method: 
        - Click the remove from favourites link on the users profile page, favourite products section
    - Expected Results:
        - The user is shown a toast confirming that the product has been removed from their favourites the product is now not listed in their favourites
    - Results:
        - The user is shown a toast confirming that the product has been removed from their favourites the product is now not listed in their favourites

4. Test: Remove a product from favourites from product list page.
    - Method: 
        - Click the remove from favourites button on the product list page.
    - Expected Results:
        - The user is shown a toast confirming that the product has been removed from their favourites the product is now not listed in their favourites
    - Results:
        - The user is shown a toast confirming that the product has been removed from their favourites the product is now not listed in their favourites

5. Test: Remove a product from favourites from product detail page.
    - Method: 
        - Click the remove from favourites button on the product detail page.
    - Expected Results:
        - The user is shown a toast confirming that the product has been removed from their favourites the product is now not listed in their favourites
    - Results:
        - The user is shown a toast confirming that the product has been removed from their favourites the product is now not listed in their favourites

_Note: The adding and removal of favourited products is accomplished via a views in the products app. If the page is slow to load and the user clicks the button again, an error occurs. I haven't thought through a fix for this yet, however, given the time I would at lesat provide some friendlier custom error pages to display_

6. Test: Products from orders are added to the user's favourite products.
    - Method: 
        - Remove any favourited products and place an order.
    - Expected Results:
        - Ordered products are shown in the user's favourite products
    - Results:
        - Ordered products are shown in the user's favourite products
    _Note: This functionality is not included in the stripe webhook so when during testing when an order was created by the Stripe webhook as opposed to the checkout app view, the order details were collected by the products were not added to favourites._

[back to top](#Testing-Documentation)

### Order History
1. Test: Place an order and check that the order is displayed user's order history
    - Method: Place an order and check the order history.
    - Expected Result: Order details are displayed in the user's order history with the most recent first.
    - Result: Order details are displayed in the user's order history with the most recent first.

2. Test: Add products from order history to basket.
    - Method: 
        1. Empty basket: Select an order is a user's order history and click re-order these products.
        2. Basket containing items: Select an order is a user's order history and click re-order these products.
    - Expected Result: 
        1. Empty basket: Items are added to the basket and the user is redirected to the basket page.
        2. Basket containing items: As with empty basket but items already in the basket are preserved
    - Result: 
        1. Empty basket: Items are added to the basket and the user is redirected to the basket page.
        2. Basket containing items: As with empty basket but items already in the basket are preserved


[back to top](#Testing-Documentation)

## Product Maintenance
1. Test: Adding a product group
    - Method: 
        1. Fill in name and profit margin and click add
        2. Fill in just name and click add
        3. Fill in just % and click add
        4. Leave blank and click add
    - Results:
        1. Test Passed. 
        2. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        3. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        4. Test Failed intially. Fixed by including required in the form fields. Test now passing.

2. Test: Updating a product group
    - Method: 
        1. Fill in name and profit margin and click update
        2. Fill in just name and click update
        3. Fill in just % and click update
        4. Leave blank and click update
    - Results:
        1. Test Passed. 
        2. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        3. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        4. Test Failed intially. Fixed by including required in the form fields. Test now passing.

3. Test: Adding a VAT group
    - Method: 
        1. Fill in name and vat rate and click add
        2. Fill in just name and click add
        3. Fill in just % and click add
        4. Leave blank and click add
    - Results:
        1. Test Passed. 
        2. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        3. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        4. Test Failed intially. Fixed by including required in the form fields. Test now passing.
4. Test: Updating a VAT group
    - Method: 
        1. Fill in name and vat rate and click update
        2. Fill in just name and click update
        3. Fill in just % and click update
        4. Leave blank and click update
    - Results:
        1. Test Passed. 
        2. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        3. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        4. Test Failed intially. Fixed by including required in the form fields. Test now passing.
5. Test: Updating a category
    - Method: 
        1. Fill in name and vat rate and click update
        2. Fill in just name and click update
        3. Fill in just % and click update
        4. Leave blank and click update
    - Results:
        1. Test Passed. 
        2. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        3. Test Failed intially. Fixed by including required in the form fields. Test now passing.
        4. Test Failed intially. Fixed by including required in the form fields. Test now passing.

6. Test: Adding a product
    - Method: Click add a product and fill out the form.
    - Expected Results:
        - Product added and searchable
    - Results:
        - Product added and is searchable
    _As mentioned in my user stories, there is a requirement for some knowledge of the data structure in order to fill out the form successfully. If the JSON format is incorrect for any of the JSONFields, the form generates and error and won't submit. Filling out the form correctly does have the desired result however I would prefer to remove the burden on the user for this aspect in future versions._

7. Test: Editing a product
    - Method: 
        - Search for a product and select edit.
        - Change the cost price.
        - Change the VAT rate group.
        - Change the product group. 
    - Expected Results:
        - Product form submits and changes are reflected in the product data.
        - Editing the cost price, VAT rate and Product group should all result in the product's price being updated.
        - Saving changes redirects the user to the product's product detail page.
    - Results:
        - Product form submits and changes are reflected in the product data.
        - Product pricing is changed upon editing the cost price, VAT rate or Product group.
        - Saving changes redirects the user to the product's product detail page.

    _As with adding a product, although this works I would prefer to make this process more user friendly_

[back to top](#Testing-Documentation)

## Content management

1. Initial Test: Prior to saving changes for the first time, the only option is to edit the primary template. Saving the form creates a custom template which indicates that the primary form is not being overwritten.
    - passed

2. Test: Saving a custom template but not selecting to make the template active.
    - Expected Result: The changes are saved to the custom template but not made active across the site.
    - Result: The changes are saved to the custom template, confirmed by examining the template on the content management page for the changes made. They are not made active across the site confirmed by examining the page to which a change was made in the custom template.

3. Test: Saving a custom template but not selecting to make the template active.
    - Expected Result: The changes are saved to the custom template and are made active across the site.
    - Result: The changes are saved to the custom template, confirmed by examining the template on the content management page for the changes made and are made active across the site confirmed by examining the page to which a change was made in the custom template.

4. Test: Making a change to the primary template.
    - Expected Result: The changes are saved to the custom template.
    - Result: The changes are saved to the custom template, confirmed by examining the template on the content management page for the change. Also confirmed by making the primary template active again and noting that the changes made are not reflected on any related pages.

5. Test: Selecting a recommended product is saved to the correct template in the correct position.
   - Method:
        1. Adding a product to position 1 in the primary template.
        2. Adding a product to position 2 in the primary template.
        3. Adding a product to position 3 in the primary template.
        4. Adding a product to position 1 in the custom template.
        5. Adding a product to position 2 in the custom template.
        6. Adding a product to position 3 in the custom template.
        7. Overwriting position 2 in the primary template with a new product.
        8. Overwriting position 1 in the custom template with a new product.
   - Expected results:
        1. Product is addded to position 1 in the primary template.
        2. Product is addded to position 2 in the primary template.
        3. Product is addded to position 3 in the primary template.
        4. Product is addded to position 1 in the custom template.
        5. Product is addded to position 2 in the custom template.
        6. Product is addded to position 3 in the custom template.
        7. Product is addded to position 2 in the primary template with a new product.
        8. Product is addded to position 1 in the custom template with a new product.
    - Results:
        1. Product is addded to position 1 in the primary template.
        2. Product is addded to position 2 in the primary template.
        3. Product is addded to position 3 in the primary template.
        4. Product is addded to position 1 in the custom template.
        5. Product is addded to position 2 in the custom template.
        6. Product is addded to position 3 in the custom template.
        7. Product is addded to position 2 in the primary template with a new product.
        8. Product is addded to position 1 in the custom template with a new product.

[back to top](#Testing-Documentation)

## Basket
1. Test: Updating the product quantity in the basket changes the product quantity correctly.
    - Method: With products in the basket:
        1. leave the quantity the same and click update
        2. increase the quantity and click update
        3. decrease the quantity and click update
    - Expected Results:
        1. The product quantity remains the same
        2. The product quantity is increased
        3. The product quantity is decreased
    - Results:
        1. The product quantity remains the same
        2. The product quantity is increased
        3. The product quantity is decreased
2. Test: Clicking remove removes a product from the basket.
    - Method:
        1. With one product in the basket, quantity 2, click remove
        2. With two different products in the basket, click remove for one of them
    - Expected Results:
        1. The product is removed from the basket and the user is prompted that their basket is empty
        2. Only the product for which remove was clicked is removed from the basket.
    - Results:
        1. The product is removed from the basket and the user is prompted that their basket is empty
        2. Only the product for which remove was clicked is removed from the basket.

3. Test: Clicking the empty basket button removes all products from the basket.
    - Method: 
        1. With one product in the basket, click empty basket.
        2. With many products in the basket, click empty basket.
    - Expected Results:
        1. The basket is emptied.
        2. The basket is emptied.
    - Results:
        1. The basket is emptied.
        2. The basket is emptied.

[back to top](#Testing-Documentation)

## Checkout
### Confirming an order with an anonymous user
1. Test: Ordering without inputting details is not possible.
    - Method: 
        1. Filling out only the card details in the order form.
        2. Leaving one blank but required field in the order form.
        3. Leaving the card details blank.
    - Expected Results:
        1. The order will not submit and the user is promtped as to why.
        2. The order will not submit and the user is promtped as to why.
        3. The order will not submit and the user is promtped as to why.
    - Results:
        1. The order will not submit and the user is promtped as to why.
        2. The order will not submit and the user is promtped as to why.
        3. The order will not submit and the user is promtped as to why.

2. Test: Filling out the required details results in a successful order.
    - Method: Using an email address from temp-mail.org
        1. Filling in all fields and card information and submitting the order.
        2. Filling in only required fields and card information and submitting the order.
    - Expected Results:
        1. User redirected to the success page and shown an order confirmation. Order confirmation sent to email address.
        2. User redirected to the success page and shown an order confirmation. Order confirmation sent to email address.
    - Results:
        1. Redirected to the success page and shown an order confirmation. Order confirmation received on temp-mail.org.
        2. Redirected to the success page and shown an order confirmation. Order confirmation received on temp-mail.org.

[back to top](#Testing-Documentation)

### Confirming an order with an authorised user
1. Test: Billing Address is prefilled upon navigating to checkout.
    - Method:
        - When logged in, add a product to the basket and navigate to check out. Check that the billing details are already filled in.
    - Expected Result: Billing address details are pre-populated.
    - Result: Billing address details are pre-populated.

2. Test: Delivery Address details are avaiable for selection.
    - Method:
        1. Without any delivery address details filled out for user, navigate to the checkout and check that the only option in the select box is to enter a new delivery address.
        2. With delivery addresses saved for the user, navigate to the checkout and check that the delivery address references are available for selection.
    - Expected result:
        1. The only delivery address option available to the user is to create a new delivery address.
        2. The user's saved delivery addresses are available for selection.
    - Results:
        1. The only delivery address option available to the user is to create a new delivery address.
        2. The user's saved delivery addresses are available for selection.
    
3. Test: Entering a new delivery address and completing the order saves the delivery address for the user.
    - Method:
        - Enter a new delivery address and complete the order.
    - Expected result:
        - The order completes and the delivery address is available to the user for selection.
    - Results:
        - The order completes and the delivery address is available to the user for selection. Confirmed both in the user profile and by navigating to the checkout page again.

4. Test: Choosing an existing delivery address and completing the order saves the delivery address for the user.
    - Method:
        - Make a change to an existing delivery address and complete the order.
    - Expected result:
        - The order completes and the delivery address is saved with the new details.
    - Results:
        - The order completes and the delivery address is saved with the new details. Confirmed both in the user profile and by navigating to the checkout page again.
    
5. Test: Choosing an existing delivery address, changing the address reference and completing the order saves the delivery address for the user.
    - Method:
        - Make a change to an existing delivery address and the address reference and complete the order.
    - Expected result:
        - The order completes and the delivery address is saved with the new adddress reference.
    - Results:
        - The order completes and the delivery address is saved with the new adddress reference. Confirmed both in the user profile and by navigating to the checkout page again.

6. Test: Not entering any delivery address and completing the order defaults to using the billing address.
    - Method:
        - Leaving the delivery address on enter new and completing the order.
    - Expected result:
        - The order completes and the billing address is used as the delivery address.
    - Results:
        - Failed. Error: Resource not found. This is being caused by the delivery forms not saving the blank form and then the view trying to get an object that does not exist, i.e. the blank form.
        - FIX: Adjusted view to use the billing address if the user does not enter a delivery address. Re-tested and test passed.


 [back to top](#Testing-Documentation)   

    