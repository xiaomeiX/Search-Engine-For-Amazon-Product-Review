from itertools import product
import os
from flask import Flask
from flask import render_template
import reviewsite.reviewsearch as solr
from flask import request
from reviewsite.forms import ReviewSearchForm
from flask import redirect
from flask import *
from flask_wtf.csrf import CSRFProtect, CSRFError


def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	csrf = CSRFProtect()
	csrf.init_app(app)

	app.config.from_mapping(
		SECRET_KEY='dev',
  		DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),

	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	###################################
	## Application code begins

	@app.route('/about', methods=['GET'])
	def about():
		return render_template("about.html")

	@app.route('/contact', methods=['GET'])
	def contact():
		return render_template("contact.html")

	@app.route('/', methods=['GET'])
	def index():
		productCount = solr.productCount()
		reviewCount = solr.reviewCount()
		return render_template('index.html',productCount=productCount, reviewCount=reviewCount )

	@app.route('/review/search',methods=['GET', 'POST'])
	def searchForm():
		form = ReviewSearchForm()
		if request.method == 'POST':
			if not form.validate():
				return render_template('reviewsearch.html', form=form)
			else:
				query = form.query.data
				return redirect(url_for('reviewResults', query = query, start=0))
		else: return render_template('reviewsearch.html', form=form)


	def getProductName(asin):
		doc = solr.productDetail(asin)['response']['docs'][0]
		if (doc==None):
			raise(f'No product return for {asin}')
		if ('title' in doc):
			return doc['title']
		else:
			raise("Asin" + asin + " no title, doc is " + str(doc))

	def list_to_dictionary(l):
		# convert : [1,2,3,4,5]
		# to: {1:2, 3:4}
		tmp_iter = iter(l)
		return (dict(zip(tmp_iter, tmp_iter)))

	@app.route('/review/results', methods=['GET'])
	def reviewResults():
		start= request.args.get('start')
		query = request.args.get('query')
		facetValue = request.args.get('facetValue')
		if facetValue == None:
			facetValue = 'overall'
		searchReturn = solr.reviewSearch(query, start, facetValue)
		docs = searchReturn['response']['docs']
		numDocs = len(docs)
		numFound = searchReturn['response']['numFound']
		for doc in docs:
			doc['productName'] = getProductName(doc['asin'])
		facetCounts = list_to_dictionary(searchReturn['facet_counts']['facet_fields']['overall'])
		return render_template('reviewresults.html', query = query,
                         start = int(start),
                         docs = docs,numFound = numFound, numDocs = numDocs, facetValue=facetValue, facetCounts = facetCounts)

	@app.route('/review/detail/<reviewid>', methods=['GET'])
	def reviewdetail(reviewid):
		idDetail = solr.id_search(reviewid)["response"]['docs'][0]
		asin = idDetail['asin']
		productDetail= solr.productDetail(asin)['response']['docs'][0]
		idDetail['productName'] = productDetail['title']
		if 'description' not in productDetail:
			idDetail['description']=""
		else: idDetail['description'] = productDetail['description']
		idDetail['price'] = productDetail['price']
		return render_template('reviewdetail.html', detail=idDetail )

	@app.route('/productreviews/<asin>', methods=['GET'])
	def productreviews(asin):
		start = request.args.get('start')
		if start ==None:
			start = 0
		facetValue = request.args.get('facetValue')
		if facetValue == None:
			facetValue = 'overall'
		reviewsDetail = solr.asin_search(asin, start=start, facetValue=facetValue)
		docs = reviewsDetail['response']['docs']
		numDocs = len(docs)
		numFound = reviewsDetail['response']['numFound']
		productName = getProductName(docs[0]['asin'])
		facetCounts = list_to_dictionary(reviewsDetail['facet_counts']['facet_fields']['overall'])
		total = 0
		for facet in facetCounts:
			total = int(facet)*int(facetCounts[facet])+total
		avgRate = int(total/numFound)
		if total/numFound-avgRate>=0.5:
			halfStar = 1
		else: halfStar =0
		rest = 5 - avgRate - halfStar
		return render_template('productreviews.html', asin=asin, start=int(start), productName=productName, halfStar=halfStar, remainStar=rest,
                         docs=docs, numFound = numFound, avgRate = avgRate, facetValue=facetValue, facetCounts = facetCounts)

	@app.route('/producAsinLookup/<proasin>', methods=['GET'])
	def producAsinLookup(proasin):
		proDetail = solr.productDetail(proasin)
		doc = proDetail['response']['docs'][0]
		proasin = doc['asin']
		return render_template('productdetail.html', proasin=proasin, detail=doc )

	@app.errorhandler(CSRFError)
	def handle_csrf_error(e): return render_template('csrf_error.html', reason=e.description), 400
	## Application code ends
	##############################
	return app
