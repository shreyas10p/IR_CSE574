import json
import urllib.request
import os
# os.chdir('VSM')
#outfn = 'path_to_your_file.txt'
#count = 1

model='bm25'
count = 1
with open('test-queries.txt', encoding="utf-8") as f:
    for line in f:
        query = line.strip('\n').replace(':', '')
        query = ' '.join(query.split()[1:])
        query = urllib.parse.quote(query)

        inurl = 'http://18.234.34.104:8983/solr/IRF20P3_BM25/select?defType=dismax&fl=id%2Cscore&q='+query+'&qf=text_en^1.2%20text_de^1.2%20text_ru^1.2&rows=20&wt=json'
        # inurl = 'http://18.212.93.250:8983/solr/IRF20P3_BM25/select?fl=id%2C%20score&q=text_en%3A'+query+'&rows=20&wt=json'
        # inurl = 'http://18.212.93.250:8983/solr/IRF20P3_BM25/select?fl=id%2C%20score&q=text_de%3A'+query+'&rows=20&wt=json'
        # inurl = 'http://18.212.93.250:8983/solr/IRF20P3_BM25/select?fl=id%2C%20score&q=text_ru%3A'+query+'&rows=20&wt=json'
        qid = str(count).zfill(3)

        outf = open(str(count)+ '.txt', 'a+')
        data = urllib.request.urlopen(inurl).read()
        docs = json.loads(data.decode('utf-8'))['response']['docs']
        rank = 1

        for doc in docs:
            outf.write(str(qid) + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + model + '\n')
            rank += 1
        outf.close()
        count += 1
