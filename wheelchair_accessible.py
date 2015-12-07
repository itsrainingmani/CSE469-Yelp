from __future__ import division
import ujson
import csv

with open('yelp_data_parsed.json', 'rb') as yelpdata:
    yelp = ujson.load(yelpdata)

cityname = []
for k, v in yelp.iteritems():
    cityname.append(k)

cities = set(cityname)

citydict = {}
geodict = {}

for city in cities:
    citydict[city] = [0,0]
    geodict[city] = []

for k, v in yelp.iteritems():
    for i in v:
        geo = []
        if i[0] == True:
            citydict[k][0] += 1
            geo.append(i[4].replace(",", ""))
            geo.append("Most Accessible")
            geodict[k].append(geo)
        else:
            citydict[k][1] += 1
            geo.append(i[4].replace(",", ""))
            geo.append("Least Accessible")
            geodict[k].append(geo)

bestacc = []
worstacc = []
for k, v in citydict.iteritems():
    total = v[0] + v[1]
    trueper = v[0]/total
    loc = (k, trueper*100)
    if (trueper*100 >= 75):
        bestacc.append(loc)
    elif (trueper*100 <= 10):
        worstacc.append(loc)
    del loc

with open('mostacc.csv','wb') as csvfile:
    mostacc = csv.writer(csvfile, delimiter=',')
    for i in range(0, len(bestacc)):
        mostacc.writerow([bestacc[i][0], bestacc[i][1]])

with open('leastacc.csv','wb') as csvfile:
    leastacc = csv.writer(csvfile, delimiter=',')
    for i in range(0, len(worstacc)):
        leastacc.writerow([worstacc[i][0].encode('utf-8'), worstacc[i][1]])


with open('geo.csv','wb') as csvfile:
    geodata = csv.writer(csvfile, delimiter=',')

    for i in range(0, len(bestacc)):
        city = bestacc[i][0]
        for address in geodict[city]:
            geodata.writerow([address[0], address[1]])

    for i in range(0, len(worstacc)):
        city = worstacc[i][0]
        for address in geodict[city]:
            geodata.writerow([address[0].encode('utf-8'), address[1]])
