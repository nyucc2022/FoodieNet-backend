# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pymysql
import json
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
    print(event)
    userEmail=event['username']
    cursor = connectDb()
    whereClause= "where `User`.`username`= '{0}'".format(userEmail)
    sql = 'use foodieNetDb'
    cursor.execute(sql)
    sql=(
        "select * from `User` "+whereClause
    )
    print(sql)
    cursor.execute(sql)
    userInfo = cursor.fetchone()
    userName=userInfo[0]
    email=userInfo[1]
    ratingtotal = userInfo[2]
    ratingtime = userInfo[3]
    rating = userInfo[4]

    result = {
        "userprofile": {
            'username': userName,
            'email': email,
            'ratingtotal': ratingtotal,
            'ratingtime': ratingtime,
            'rating': rating
        }
    }

    return {
        "statusCode": 200,
        "headers": {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(result)
    }



