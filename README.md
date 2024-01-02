# Search-Engine-For-Amazon-Product-Review
Information Retrieval and Search for Amazon Product Review

In this project, will build a web application that will use SOLR to deliver search Amzon results
and product and review details. Will build on your SOLR implementation and the code we built in Flask Server, but there will be some differences, explained below.
The website will have five page types:

A gateway page – a very simple page providing some text and a link to the search page.
Review search: search for product reviews using keywords.
Review search results: summary information about reviews that match the review
search query from the review search page. The review search results page will also
involve some new SOLR features: pagination, faceting, and query suggestion.
Review detail: more detailed information about a single review
Product detail: more detailed information about a product
Compared to Another Web app:

The gateway page is new, but simple.
The review search page is simple without the dropdowns to filter on date and score.
The search results page plays has new features like pagination and faceting
The review and product detail pages just display information about a single review or product with rank.
Documents – the new Review Data Set
Read review and product information from data files. There is one data file for review information and one data file for product information. These two files are joined on a field asin. There is more information about the data files and their format in the Jupyter Notebook. The data files and notebook are all in the folder.

Search Types
The search types are simpler – for example, we won't do special phrase search on the product name and won't do filtering on review score or review data. There will only be three search/retrieval use cases.

Search for reviews matching keywords – you can use standard SOLR text analyzers and keyword
matching to do this search, and you should search on words in the review summary and the
review body. (These fields are defined in the Jupyter Notebook.)
Lookup by review ID to get review details
Lookup by product ID (asin) to get product details
Review Information versus Product Information
For this project, we have more information about products – for example the name, a description, the price, the sales rank, and browse categories. I store some of these product attributes to render a product detail page. User
are not allowed to put product information for a review in the document with the review itself – that would mean that the product information might be stored redundantly thousands of times, which is an unacceptable waste of space.
To avoid this redundant storage, User will build two different and separate SOLR collections: one to store reviews and one to store products. The trick will be that sometimes to render a page code will
have to make two calls to SOLR, one to get review information and the second to get product information. That’s no problem, remember that SOLR service can have two active collections, and when do a search request to SOLR specify the collection to search against.
The most common example that user will see below is that the review search results page displays the product name. To get search results, first query against the reviews collection and get a list of “review documents.”

The review document has the product ID (ASIN), but not the product name, and the product name must appear in the review search result line (see mockup below). So then user need to make a second SOLR call to the products collection, keyed by ASIN, so user can get the product name, which user then display on the review search results page along with data about the review. This is a really common practice in composing pages in a search application – when Amazon renders a product detail page for example, it makes calls out to many different services to pull together all the information that is on the page.

Steps to Take
The assignment divides into two main parts

Parsing and indexing the review and product data. User will be reading data from files. Only the functions that parse data from the product and review data files and for each creates a dictionary that can be passed to SOLR for indexing.
The web app that takes search requests and renders information about search results and review and product details. The deliverable for this phase is a Flask application that calls SOLR to get information about reviews and products, then renders that information.
Web Page Types
This document contains more detail about each of the page types. Each includes a screen shot – these screen shots indicate content only – I created the web page and make them more stylish.

Folder file including:

A Jupyter notebook containing the code that defines functions to parse the product and review data
Two folders containing configuration for your two SOLR collections. The names for these configuration directories and the SOLR collections are specified in the Jupyter Notebook.
A single folder named reviewsite containing Flask application. The application may assume that SOLR will be running on localhost:8983 and that document collections will have been created and indexed prior to starting Flask
A file retrospective.pdf.
