import pymysql
dbHost= 'database-1.cu5fl7egwb38.us-east-1.rds.amazonaws.com'
dbUserName= 'admin'
dbPassword= 'asdf1234'
dbName= 'database-1'
dbPort = 3306

import pymysql

dbHost = 'database-1.cu5fl7egwb38.us-east-1.rds.amazonaws.com'
dbUserName = 'admin'
dbPassword = 'asdf1234'
dbName = 'database-1'
dbPort = 3306


def connectDb():
    db = pymysql.connect(host=dbHost, user=dbUserName, passwd=dbPassword)
    cursor = db.cursor()
    return (cursor, db)


def lambda_handler(event, context):
    try:
        print(event)
        print(context)
        userEmail = event['context']['email']
        (cursor, db) = connectDb()
        sql = 'use foodieNetDb'
        cursor.execute(sql)
        sql = (
            "select * from `User` where `User`.`email`= '{0}'".format(userEmail)
        )
        print(sql)
        cursor.execute(sql)
        userInfo = cursor.fetchone()
        groupId = event['body']['groupID']
        userName = userInfo[0]
        sql = (
            "select * from `GroupUser` where `GroupUser`.`username` = '{0}' and `GroupUser`.`gid` = '{1}'".format(
                userName, groupId)
        )
        cursor.execute(sql)
        info = cursor.fetchone()
        if info[3] is True:
            return
        else:
            sql = (
                "update `GroupUser` set Reviewed= True where gid = '{0}' and username = '{1}'".format(groupId, userName)
            )
        cursor.execute(sql)
        groupUsersLs = event['body']['groupUsers']
        for user in groupUsersLs:
            sql = (
                "update `User` set ratingtotal = ratingtotal + {0}, ratingtime= ratingtime+1, rating=ratingtotal/ratingtime  where username = '{1}'".format(
                    user['star'], user['userName'])
            )
            cursor.execute(sql)
            db.commit()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }

        }

