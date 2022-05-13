# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pymysql
dbHost= 'database-1.cu5fl7egwb38.us-east-1.rds.amazonaws.com'
dbUserName= 'admin'
dbPassword= 'asdf1234'
dbName= 'database-1'
dbPort = 3306

def connectDb():
    db = pymysql.connect(host=dbHost, user=dbUserName, passwd=dbPassword)
    cursor = db.cursor()
    return cursor


def lambda_handler(event, context):
    # Use a breakpoint in the code line below to debug your script.
    result=[]
    cursor=connectDb()
    nameCondition = "Restaurant.name like '%{0}%'".format(event['name'])
    cuisineCondition=''
    whereClause='where '
    for cuisine in event['cuisine']:
        cuisineCondition+="Restaurant.cuisine= '{0}' or ".format(cuisine)
    if len(event['name'])==0 and len(event['cuisine'])!=0:
        whereClause += cuisineCondition[0:len(cuisineCondition)-4]
    elif len(event['name'])!=0 and len(event['cuisine'])==0:
        whereClause += nameCondition
    elif len(event['name'])!=0  and len(event['cuisine'])!=0:
        whereClause+=nameCondition+" and ("
        whereClause+=cuisineCondition[0:len(cuisineCondition)-4]+")"
    else:
        whereClause=''
    print(whereClause)
    sql='use foodieNetDb'
    cursor.execute(sql)
    if whereClause=='':
        sql="select * from `Restaurant`"
    else:
        sql=(
            "select * from Restaurant "+ whereClause
        )
    sql+= " limit 100"
    print(sql)
    cursor.execute(sql)
    for info in cursor:
        print(info)
        res={
            'rid': info[0],
            'name': info[1],
            'cuisine': info[2],
            'address': info[3],
            'zipcode': info[4],
            'longitude': info[5],
            'latitude': info[6],
            'image': info[7]
        }
        result.append(res)

    print(result)
    return result
       


