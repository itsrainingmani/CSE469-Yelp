import ujson, json
import sets
import io

busdata = []
with open('business.json', 'rb') as bus:
    for line in bus:
        business = ujson.loads(line)
        busdata.append(business)

print "Opened Yelp JSON file"

citydict = {}
citylist = []
for business in busdata:
    citylist.append(business['city'].lower())

cities = set(citylist)

for city in cities:
    citydict[city] = []

for business in busdata:
    for i in business['categories']:
        if i == "Restaurants":
            yelpdata = []
            if (business['attributes'].has_key("Wheelchair Accessible")):
                yelpdata.append(business['attributes']['Wheelchair Accessible'])
            else:
                yelpdata.append(False)
            yelpdata.append(business['review_count'])
            yelpdata.append(business['stars'])
            yelpdata.append(business['name'])
            yelpdata.append(business['full_address'].replace("\n", ' '))

            citydict[business['city'].lower()].append(yelpdata)

print "Finished Preprocessing"

print len(citydict)
for k, v in citydict.items():
    if len(v) == 0:
        del citydict[k]

print len(citydict)

with io.open('newdata.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(citydict, ensure_ascii=False)))

print "Wrote dict to file"
