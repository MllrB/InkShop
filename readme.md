# The InkShop 
##### An E-Commerce Site by MllrB
##### Developed for CodeInstute Milestone Project 4 - Full Stack Development with Django

The InkShop is a basic e-commerce solution which allows...
 - Customers 
    - to browse and purchase products
    - to login and create a profile
    - to login with Google using their gmail account
 - Staff
    - Add and edit products
    - Select products to be featured on the landing page

You can visit the deployed web app via:
- [Heroku](https://ci-ms4-inkshop.herokuapp.com/)

Files and code can be found in my GitHub repository:
- [GitHub Repository](https://github.com/MllrB/InkShop)

## Contents

## UX

### Project Goals
My goal for this project was to learn more about creating web apps using the Django framework and to create a basic ecommerce solution to service my current work environment, the sale of printers and their consumables. 

### User Stories
#### Customers User Stories

As a customer I would like to...
##### Regarding Products
1. browse products by category.
    - Using the browse icon to the left of the main search in the navbar, users can select from three high level categories under which more specific categories are shown. From these users can navigate to products contained within these categories. The higher level categories are simply stored as a character field in the categories model with the values of 'supplies', 'printers' and 'accessories'. To improve on this, I would implement these higher level categories as a seperate model and link to the lower level categories via a foreign key field in the lower level categories model. With this implemented, I would be able to add a feature for the site owner to add/edit the high level categories and therefore also which lower level categories they contain. This would allow greater flexibility for the site owner to structure their site with regards to how a user could navigate to products by browsing.
2. search for products by product code or description.
    - When the user searches a for product, their search term is queried against product SKUs, title, description and, in the case of supplies, against a list of related printers (see [Site Data](#Site-Data) for an explanation on the related printers field). This setup should be enough to find most searches, however, product data can be inconsistent. Products may have more than one SKU, for example, a Brother ink SKU might or might not contain a hyphen: LC223BK vs LC-223BK. In this example, the data source I used uses the hyphenated version and as such is stored in the db with a hyphen. In future versions I would add a custom mananger to the Product model to remove special characters like hyphens when processing search queries.
3. filter my searches by product feature, eg color, size etc.
    - As with the search queries above, the data set I used is inconsistent with regards to product features. With this in mind I hand picked product features that I felt were relevant and hard coded these into the filtering function. This works for the purposes of this data set, however, it is not ideal in terms of re-usability or future proofing. My solution to this would be to include all the features.
4. find cartridges for my printer.
    - Ideally I would have liked to include separate models containing printers and supplies and to link them via a many to many field, however, as discussed in the [Site Data](#Site-Data) section below, this is not feasible for the resources available to me for this project. As a workaround, I included the related_printers field in the product model which is included in querying user searches. This feature currently only applies to supplies and a downside is that if the printer is not contained in the related printers field, the query won't find it. For future versions, I would change this field to related products and allow staff users to add related products to the field.
5. be shown products related to the product I'm viewing.
    - This is working for supplies based on entries in the related printers field that are common to each product. As above, for future versions I would extend this to all products and allow staff users to manage common products.
6. see clearly the excluding and including VAT prices for products.
    - To achieve this, each product price is stored excluding VAT and the model makes use of a vat rate field, percentage determined by membeship of a VAT group, and a method to calculate the inclusive of vat price for each product. Both prices are displayed for each product on the product list and detail pages. The shopping basket, checkout and order histories show product prices excluding VAT with the total VAT for the basket/order displayed in the totals section.

##### Regarding Accounts
1. be able to create an account.
    - Users have two methods by which they can create an account. 
        - The first, by entering their email address and chosen password. At this point they are sent a link to verify their email address and on verification are redirected to their profile page where they can add extra information.
        - The second by logging in with Google. This is acheived using the Django AllAuth social account model with Googel included as a provider. Upon login, a Social Account, User Account and UserProfile are created for the user and the user is redirected to their profile page. Their email address, full name and profile pic are automatically stored in their UserProfile and they can add further information on the profile page.
2. store my information for easier/faster ordering.
    - On the profile page, users can fill out their billing address and also multiple delivery addresses if they wish. Upon checkout, they will have to store at least one of these addresses in full (excluding fields not required) and their information will be updated automatically.
3. be able to view my order history.
    - On the profile page, users can view their order histories by complete order. They can also repeat entire orders using a button that adds the same products and quantities from the order to the shopping basket. The basket is added to as opposed to overwritten so if there are products already in the basket, they will not be removed.
4. be able to download previous invoices/receipts.
    - Unfortunately, I have had to leave this for future versions, to be achieved using the ReportLab library.
5. store multiple delivery addresses.
    - Users can store multiple delivery addresses with their profile and access them on the checkout page. Each delivery address requires an address reference to be entered. This reference is required to be unique per user i.e. two different users can each have a 'work' delivery address but a single user cannot have two 'work' delivery addresses.
6. save favourite products for faster re-ordering and in case I forget my printer model.
    - When logged in, users can save products to their favourites by clicking the heart icon on the product list and detail pages. Any products that the user has ordered will also be added to the users favourites at the point of ordering. Favourited products can be removed via the favourite products section of their profiles or from the product list and detail pages.
7. upload and store my VAT exemption cert with my profile.
    - This is another that will need to be implemented in future versions and is dependant on some of the unimplemented site owner user stories.
##### Regarding Ordering
1. see clearly the delivery cost my order will incur if any.
    - The delivery cost is shown on the shopping basket, checkout, checkout success and, in the case of logged in users, on the order history pages. The cost is also shown in the shopping basket toast that can be accessed by hovering over the shopping basket icon. On the shopping basket page, the user is prompted to spend x amount more to get free delivery.
2. see clearly the overall cost of my order.
    - The order grand total is displayed on the shopping basket page and toast, checkout and checkout success pages, and in the users order history in the case of a logged in user. On each of these pages the order cost is broken down into sub total, total VAT, delivery cost and grand total. Te order grand total is also displayed underneath the shopping basket icon at the top right of the site.
3. be able to easily adjust my basket before completing my order.
    Each line in the basket can be added to or removed from the shopping basket on the shopping basket page which can be accessed by clicking the basket icon at the top right of the site. The user also has the ability to empty the basket in it's entirity.
4. to order without having to pay VAT.
    - This is another for future versions and depends on the implementation of some site owner user stories. This user story is in reference to customers that are exempt from paying VAT. Login would be required and on implementation, customers would be shown only excluding VAT prices and shopping basket/order totals would be adjusted accordingly.
5. order with a purchase order reference.
    -  This is another for future versions and depends on the implementation of the site owner user story regarding the creation of credit account customers. Dependant on the background infrastructure being implemented, customers would be given the option of paying for orders by card or by simply entering a purchase order number. Login would be required.

#### Site Owner User Stories
As a the site owner i would like to...
##### Regarding Products
1. be able to add products.
    - This is implemented via the product maintenance section of the website and is accessible via the account icon to the right of the site navigation search bar. Users are required to be logged in and staff/super users. The user is shown a form with all the fields neccessary to create a product. As it stands, this is a basic version of the product form and requires the user to have knowledge of the data structure, for example, product features are stored in a JSONfield so the user would need to be aware of the syntax required to add a product feature. In future versions, I would design a custom form and build the product form on the server side to take this type of requirement away from the user.
2. be able to amend product descriptions.
    - Staff users can edit products in the product maintenance section of the site. They first need to search for products and then select the product they wish to edit. At this point they are shown a prepopulated product form. In the case of descripiton, little knowledge requirements are placed on the user, however, the field is made HTML safe on the client side using the Django's 'safe' template filter so a basic knowledge of html would supplement the user's ability to format the description to their pleasing.
3. be able to amend product categorisation.
    - Also available via the edit product section of product maintenance, users can choose which cateegory a product should belong to. This is another reason why in future versions I would implement a two tiered categorisation structure which would allow greater flexibility for staff users to structure their data. Currently, staff users can edit category titles and descriptions but not which type of product they refer to which means that moving products from category to category is dependent on users making sensible decisions.
4. be able to amend product pricing.
    - Each product is a member of a product group and each product group has a profit margin percentage associated with it. Product prices are updated when the product is saved or there is an 'update prices' button on the product maintenance page which updates all product prices. The price is calculated from the cost price and the profit margin to be applied. With this in place, users have a number of options for updating prices...
        1. Users can add new product groups with whatever profit margin percentage they choose and then add products to that group to calculate the new prices.
        2. Users can move products from one product group to another.
        3. Users can update the margin percentages of existing product groups and update all prices.
    In addition, users can also adjust the product cost price.
5. be able to add categories.
    - Unfortunately, I left this too late and ran out of time to include it in 
6. be able to set VAT rates.
    - Similar to product groups, each product is a member of a VAT group which determines the rate of VAT applied. The functionality is there, however, at the moment it is not being fully applied. In future versions, customers would also be members of a VAT group (set to a default) which would allow for VAT exempt customers or customers outside the site owner's VAT jurisdiction. 
7. be able to manage content on the website.
    - I have included a content managment section on the site, accessible to staff via the account icon. In this section, users can update the content on the site information pages (about, delivery info, FAQs, Ts & Cs, privacy policy) as well as change the products displayed in the 'recommended by us' section of the landing page. There are two templates for users to access, 'primary' and 'custom'. Regarding the information pages, no changes are saved to the primary template in order to preserve this as a backup in case mistakes are made. All changes to either template are saved to the custom template. Recommended products can be changed on either template and the user can choose which template to use. 
    In future versions, I would also allow the user to add new templates.

##### Unfulfilled Site Owner User Stories
I also had set myself some ambitious targets for site owner user stories that in hindsight were unrealistic given my working knowledge of the django framework vs the time frame in which to complete this project. Should I continue working on this particular project outside of my coursework with the Code Institute, I would implement these in future versions. These user stories are;

As a the site owner I would like to...
- be able to see and amend customer details
- be able to create credit accounts
- be able to create credit account orders
- be able to see customer order history
- be able to add and maintain supplier details
- be able to run a price/stock feed
- be able to see and amend current in house stock and see what stock is available from suppliers
- be able to mark orders as shipped, print a delivery docket and notify the customer that the order has shipped.
- be able to take orders over the phone by selecting a customer and completing the order for them
- be able to cancel/refund orders
- be able to run a price/stock feed
- be able to see newly added products
- be able to amend product, category, product group and vat groups via csv export and import

### Design Choices
I wanted the site to look clean and uncluttered so I decided to use a combination of greys and white colours for the background and product cards. The logo closely matches the Bootstrap success colour so I used that for most of the site's buttons and navigation icons. 

I wanted to use fonts that complemented this clean look and feel and from a number of options I settled on:
 - Headings: [Google Fonts - Marvel](https://fonts.google.com/specimen/Marvel)
 - Text and links: [Google Fonts - Raleway](https://fonts.google.com/specimen/Raleway)

Logo: A slightly modified version of my employer's logo.

## Wireframes
[PDF version](/media/wireframes.pdf)

These wireframes were useful, however, I did make some design decisions on the fly. 
- I thought that the product management page could be condensed and that the user would be better served without an extra menu layer to navigate. To change this, the edit/add product group, edit/add vat group and edit categories are included on the main product maintenance page. I am happy with this decision as far as the desktop view goes. In terms of the mobile view, the choice I made for the layout of the page does not suit smaller screens. It is my opinion that staff users are more likely to use desktop devices so I decided to come back to this to fix the mobile views if I had time. Unfortunately, I did not. To fix this, I would redesign the page so as not to use tables but instead to use a combination of form groups and select boxes to allow users to choose which groups/categories to amend and save. This would make the mobile view automatically more responsive.
- I had initially planned for the filters functionality on the product list pages to be a collapsible menu that would slide out from the left on desktop views and be contained within a fixed button on mobile views. I decided that this was unneccesary for desktop views and that the filters could be displayed alongside the products. On mobile views, i struggled with finding a space for this button and left this functionality out. This again is due to a time constraint and I would include this feature in future versions.
- I switched the order of optional extra/related products and the product information tabs on the product detail pages.
- I decided to include optional extras/related products on the basket pages.
- I did not consider the browse categories pages in my initial plans. For the most part they are fine, however, for future versions I would make a small change to accomodate cases where there are less than four categories (desktop views). Specifically in the case of the accessories categories, there are only two categories and these are left aligned when viewed on desktop devices. I  would prefer them to be centered.
- I decided against using modals as a layer of protection against deleting user delivery addresses or favourites. I thought it too much given that the information being removed is not of major importance and could be added again by the user quite easily.

## Site Data

All the data on the site was initially provided by [IceCat](https://icecat.biz/) using their open catalogue. For free users they provide xml and csv download and access to their Computers & Peripherals catalogue.

My initial plan was to import product files for all products within selected categories and to be able to update these products automatically or at the click of a button. I soon discovered that this would not be feasible as the product file itself is just shy of a couple of million lines and I don't have access to equipment that could handle the memory allocation requirements to parse this size of file. My solution was to split the file manually into 17 separate csv files and to extract the data I needed from these separate files. As solutions go, it was a bit clunky and definitely not geared towards automation. To extract the products I wanted, I decided to compare the IceCat data against a dataset from my current employers (which I have been maintaining manually for years) and also to include only products from ceratin manufacturers that had been added to the IceCat catalogue after 2017. This process provided me with 1694 products. Plenty! At this point the data only included some SKUs and IceCat product IDs, the IceCat product IDs have become the primary keys for all the products in my Product model. To gain further data such as product features, img urls, titles, descriptions, summaries etc... I wrote a script to download and parse xml files from IceCat. For pricing, I included (adjusted) cost prices from my employer's dataset for any products that matched.

I had also intended on including a supplies finder on my homepage, however, this would've have generated tens of thousands of rows in the database, even if I excluded any references irrelevant to my dataset. This became unfeasible since I planned to deploy using Heroku and had learned that the Heroku Postgres Hobby Dev (free!) plan also carries with it some restrictions - 10000 rows in the database and 1gb storage ([Heroku Doc](https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier)). My workaround was to include a related printers field for supplies in my product model and to include this in search queries. The related_printers field data was built up using a combination of the IceCat data and from my employers dataset.

## Deployment
This project has been deployed using Heroku.
- [Heroku Deployment](http://ci-ms4-inkshop.herokuapp.com/)

### Initial Steps
After logging into my Heroku dashboard via [Heroku's login page](https://id.heroku.com/login), I selected "Create new app" from the dropdown menu at the top right of the dashboard. I typed in my project name and selected Europe as my region. The deployment method was set to Heroku Git by default so I left that as is. I then navigated to the Settings tab and clicked "Reveal Config Vars". I added a SECRET_KEY config variable to contain a django secret key which I obtained from django key generator - [miniwebtool](https://miniwebtool.com/django-secret-key-generator/).
From the command line, I initialised a git repository and established a connection to Heroku using the "heroku git:remote -a " command with my application name. I created a requirements file using the pip freeze command and also created a Procfile. 
In the deploy tab of my Heroku dashboard, I connected to my GitHub repository so that my git push commands would be automatically pushed to Heroku.
Under the resources tab of the Heroku dashboard, I added Heroku Postgres as an addon and provisioned Heroku Postgres database under the Hobby Dev plan. This added a DATABASE_URL config variable to my settings which I then copied to my local environment and stored it in an env.py file that would not be pushed to GitHub or Heroku. In my local environment, I added a condition to use the DATABASE_URL if it was present in my environment and to use dj_database_url to parse the database key. I had previously installed dj_database_url during the coursework so it was not necessary for me to install it again.
At this point, I ran a git push and once the build had completed on Heroku, I ran all the migrations. After the migrations were complete, I used the 'python manage.py loaddata' command to load my fixtures to the database. 

### Secondary steps
#### Setting Up an AWS bucket
I set up an Amazon Web Services bucket to store my static and media files. To do this...
- I logged in to my AWS Management Console
- Searched for and selected the S3 service
- Clicked 'Create Bucket' and gave it a name
- Allowed all public access under the permissions tab and clicked the acknowledgement
- Under the CORS Configuration tab I copied in a CORS Configuration (from the boutique ado example)
- Under the Bucket Policy I generated a new policy using my ARN code
- I next selected services and searched for and selected IAM
- From there I added a new user and selected programmatic access
- I then created a new group with AmazonS3FullAccess Policy and added the new user to the group
- After creating the user, I was given an access key and secret code
- I then opened the group policy and amended the Resource section to include my bucket's ARN code
Both the Access Key and Secret Codes needed to be stored in the Config Vars of my Heroku app.

#### Setting up Stripe
I already have an account with Stipe so I logged my dashboard from where I could get my public and secret keys from the developers>API keys section. I then needed to setup a webhook endpoint from developers>webhooks. I entered my endpoint url, gave it a description and selected all events. With this done, I had access to a webhook secret key.
The three keys I obtained had to be included in my Config Vars in the settings tab of my Heroku app dashboard.

#### Setting up Login with Gmail
With my account logged in, I navigated to the [console](https://console.developers.google.com/) from where I clicked Enable APIS & Services. From there I selected the Gmail API. I then needed to create credentials in which I could include my Heroku App as and authorised URI and also create an authorised redirect URI - accounts/google/login/callback/.
From here I was able to get my Client ID and secret keys. Next I needed to login to the admin section of my deployed site and select Social Account Applications. Then I could select Google as a provider (from including allauth.socialaccount.providers.google as an INSTALLED_APP in my settings.py file) enter my two keys and choose the site name (default is example.com).

### Final Step


#### Issues Encountered
I used vscode on my computer as my development environment rather than Gitpod. An effect of this is that I needed to deploy to Heroku earlier than might have been otherwise necessary in order to set up webhooks from Stripe (they require a genuine url as an endpoint). As a result of this, I found that I needed to run migrations to the deployment database more regularly as my models changed and were added to. To achieve this I was commenting/uncommenting the DATABASE_URL variable in my env.py file as needed. This got a bit confusing and I think it caused me more problems than it ought along the way. For example, I had an error in my fixtures file where a primary key had been repeated and as a result many of my products were missing. This didn't seem to be happening for my development site as I had loaded a previous fixture data to it, however, I thought it was something I was doing wrong with my models and migrations. To try and fix it (before I had found my error) I reverted all migrations to zero for the deployment site and migrated from scratch. I have since learned that there is better way to load fixtures and run migrations to the deployment database, by using the 'heroku run python manage.py ' command. 

### CONFIG VARS
The Config Vars required for this application are:
- SECRET_KEY  :  _A Django secret key_
- DATABASE_URL  :  _A Postgres database URl_
- STRIPE_PUBLIC_KEY  :  _A Stripe publishable key_
- STRIPE_SECRET_KEY  :  _A Stripe secret key_
- STRIPE_WH_SECRET :  _A Stripe Webhook secret key_
- AWS_ACCESS_KEY_ID  :  _AWS User Access Key_
- AWS_SECRET_ACCESS_KEY  :  _AWS Sercet Key_
- USE_AWS: _set to true for deployment environment_
- EMAIL_HOST_PASS: _A key provided by Google to allow smtp service_
- EMAIL_HOST_USER: _An email address_



## Technologies Used

#### Languages
* HTML
* CSS
* Javascript
* Python
* Django Template

#### Libraries/Tools/Packages
* Django Framework
* Django AllAuth
* Django CrispyForms
* Django Countries
* Django Stroages
* dj-database-url
* gunicorn
* psycopg2
* boto3
* pillow
* jQuery
* Bootstrap 4
* Google Fonts
* Git

#### Applications
* Visual Studio Code
* GitHub
* Heroku
* Adobe Photoshop


## Cloning my GitHub Repository
Should you wish to clone this repository you can do so by:
1. Navigate to my [InkShop](https://github.com/MllrB/InkShop).
2. Click the green "Code" button on the right side of the repository.
3. Copy the URL displayed `(https://github.com/MllrB/InkShop.git)`.
4. You will need to have Git installed on your system, if you don't, you can find out how [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
5. Open a terminal window and navigate to the folder where you wish to clone this repository.
6. Initialise Git for this folder by typing "git init".
7. Type "git clone " followed by the URL you copied on step 3. It should look like this...
    - `git clone https://github.com/MllrB/InkShop.git`


## Acknowledgements
* All product images and data are provided by [IceCat](https://icecat.biz/)
* The InkShop logo is owned by [theinkshop.ie](http://www.theinkshop.ie/)
* The Code Institute Boutique Ado project has been used as a reference and guide
* Fonts provided by [Google Fonts](https://fonts.google.com).