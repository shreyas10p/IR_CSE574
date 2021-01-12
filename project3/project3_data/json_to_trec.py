# -*- coding: utf-8 -*-


import json
# if you are using python 3, you should
import urllib.request
# import urllib2


# change the url according to your own corename and query
inurl = 'http://ec2-34-228-160-216.compute-1.amazonaws.com:8983/solr/IRF20P3_BM25/select?fl=id%2C%20score&q=text_de%3AASYL-FL%C3%9CCHTLING%20bedankt%20sich%20per%20Video-Botschaft%20bei%20Til%20Schweiger&rows=20&wt=json'
outfn = '4.txt'

# change query id and IRModel name accordingly
qid = '012'
IRModel='BM25' #either bm25 or vsm
outf = open(outfn, 'a+')
# data = urllib2.urlopen(inurl)
# if you're using python 3, you should use
data = urllib.request.urlopen(inurl)

docs = json.load(data)['response']['docs']
# the ranking should start from 1 and increase
rank = 1
for doc in docs:
    outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
    rank += 1
outf.close()
