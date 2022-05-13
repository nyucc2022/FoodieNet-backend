# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pymysql
import requests
dbHost= 'database-1.cu5fl7egwb38.us-east-1.rds.amazonaws.com'
dbUserName= 'admin'
dbPassword= 'asdf1234'
dbName= 'database-1'
dbPort = 3306
yelpApi_key='G3jM6RS_HAHNlCo7v3dMELB81n-j8j8WGV-hs8dUimI7YoL3RIpMlSNZwwIhYHPQDNDzHZ0_Y0KoBjnXDYu_2W9bFifI_OX68Z2NZtPoGeGc1isANUMGzjP5hSEZYnYx'
location= 'Manhattan'
headers = {
    'Authorization': 'Bearer {0}'.format(yelpApi_key)
}
def connectDb():
    db = pymysql.connect(host=dbHost, user= dbUserName, passwd=dbPassword)
    cursor= db.cursor()
    resDic=scrapeData()
    storeDatatoDB(resDic,cursor,db)


def scrapeData():
    cuisineList = ['Native', 'Maxican', 'Japanese', 'Chinese']
    resDic = {}
    for cuisine in cuisineList:
        businessCount = 0
        for offset in range(0, 1000, 50):
            url = 'https://api.yelp.com/v3/businesses/search?location={0}&limit=50&offset={1}&categories={2}'.format(location, offset,cuisine)
            yelpData = requests.get(url, headers=headers)
            jsonYelpData = yelpData.json()
            for business in jsonYelpData['businesses']:
                rid='{0}'.format(business['id'])
                if rid in resDic.keys():
                    continue
                else:
                    name= business['name']
                    cuisine= cuisine
                    address= '{0}'.format(business['location']['display_address'][0])
                    zipcode='{0}'.format(business['location']['zip_code'])
                    longitude= '{0}'.format(business['coordinates']['longitude'])
                    latitude='{0}'.format(business['coordinates']['latitude'])
                    image='{0}'.format(business['image_url'])  ## maybe null
                    if image == '':
                        print("image is NULL")
                    businessCount+=1
                    rest = {
                        'rid': rid,
                        'name': name,
                        'cuisine': cuisine,
                        'address': address,
                        'zipcode': zipcode,
                        'longitude': longitude,
                        'latitude': latitude,
                        'image': image
                    }
                    resDic[rid]=rest
        print(businessCount)
    return resDic


def storeDatatoDB(resDic,cursor,db):
    sql = 'use foodieNetDb'
    cursor.execute(sql)
    for key in resDic.keys():
        rest= resDic[key]
        sql="insert into `Restaurant` (`rid`, `name`, cuisine, address, zipcode, longitude, latitude, image ) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        val=(rest['rid'],rest['name'], rest['cuisine'], rest['address'], int(rest['zipcode']), float(rest['longitude']), float(rest['latitude']), rest['image'])
        cursor.execute(sql,val)
        # db.commit()

    sql = 'select * from `Restaurant`'
    cursor.execute(sql)
    for x in cursor:
        print(x)











            # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    connectDb()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
