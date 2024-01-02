import requests
from importlib import reload


def reviewSearch(query, start=0, facetValue=None):
    return do_review_query(query_dictionary(query, start=start, facetValue=facetValue))

def productSearch(query, start=0):
    return do_product_query(query_dictionary(query, start=start))

def productDetail(asin):
    return do_product_query(asin_prod_dictionary(asin))

def asin_search(asin, start=0, facetValue=None):
    print(f'asin: {asin}')
    return do_review_query(asin_query_dictionary(asin=asin, start=start, facetValue=facetValue))

def id_search(id):
	return do_review_query(id_query_dictionary(id))

def productCount():
    return do_product_query({'q':'*:*', 'rows':0})['response']['numFound']

def reviewCount():
    return do_review_query({'q':'*:*', 'rows':0})['response']['numFound']


def do_review_query(params, port="8983", collection="reviews"):
    print(params)
    param_arg = "&".join(list(map(lambda p: f"{p[0]}={p[1]}", list(params.items()))))
    query_string = f"http://localhost:{port}/solr/{collection}/select"
    print("Param " + str(params))
    r = requests.get(query_string, param_arg)
    if (r.status_code == 200):
        return r.json()
    else:
        raise Exception(f"Request Error: {r.status_code}")

def do_product_query(params, port="8983", collection="products"):
    param_arg = "&".join(list(map(lambda p: f"{p[0]}={p[1]}", list(params.items()))))
    query_string = f"http://localhost:{port}/solr/{collection}/select"
    print("Sending query " + query_string)
    print("Param " + str(params))
    r = requests.get(query_string, param_arg)
    if (r.status_code == 200):
        return r.json()
    else:
        raise Exception(f"Request Error: {r.status_code}")

def id_query_dictionary(id):
	return {"q": f"id:{id}"}

def asin_prod_dictionary(asin):
    return {"q": f"asin:{asin}"}

def asin_query_dictionary(asin="", start=0, facetValue=None):
    num = "*"
    if ":" in facetValue:
        field= facetValue.strip().split(":")
        facetValue = field[0]
        num = field[1]
    query = f'asin:{asin}'
    fq = f'overall:{num}'
    return {"q": query, "start": start, "facet.field":facetValue,"fq":fq, "facet":"true"}


def query_dictionary(query="", start=0, facetValue=None):
    if len(query)>0:
        param_arg = ''
        temp = query.split()
        for i in temp:
            param_arg +=  str(i) + "+"
        query = param_arg
    num = "*"
    if ":" in facetValue:
        field= facetValue.strip().split(":")
        facetValue = field[0]
        num = field[1]
    fq = f'overall:{num}'
    return {"q": query, "start": start, "facet.field":facetValue,"fq":fq, "facet":"true"}




