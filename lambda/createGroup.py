import pymysql
import json
import jwt
from datetime import datetime

dbHost= 'database-1.cu5fl7egwb38.us-east-1.rds.amazonaws.com'
dbUserName= 'admin'
dbPassword= 'asdf1234'
dbName= 'database-1'
dbPort = 3306


def connectDb():
    connection = pymysql.connect(host=dbHost, user=dbUserName, passwd=dbPassword)
    cursor = connection.cursor()
    return connection, cursor

def lambda_handler(event, context):


    # get ownername using token from cognito
    # for testing locally you can enter the JWT ID Token here
    # eventToken = {'token': 'eyJraWQiOiIybXlqZUZ1dlZnakJCWjNLVmJhYmg2MkFHTWpJM1BuTTlIbW4zY3ZaZFFZPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI5NzA5ZTkyMC1mZGI2LTQ1YWItODY2NC1kZjBkYmNmMmY3MTYiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX21URlk1UGFOZyIsImNvZ25pdG86dXNlcm5hbWUiOiJ0ZXN0Iiwib3JpZ2luX2p0aSI6IjBlYjhjZDVjLTViNGEtNGI4NC1hOGI2LTRiNzUwNTdiOGE4NyIsImF1ZCI6IjFuYWEwaW9wY2p1aTgyNTU1NXNxajI0dnZsIiwiZXZlbnRfaWQiOiJjMGJiZmNmZS1lYzA1LTQxNmMtYjlmYy00ZDVjMDk4NjI4YTQiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY1MTk3NzQ1MCwiZXhwIjoxNjUxOTgxMDUwLCJpYXQiOjE2NTE5Nzc0NTAsImp0aSI6ImIwZmIxMThjLWRiMDItNDk4OS04YTlhLTlmNjNjZDNjM2Q0NiIsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9.EydsFi3UwFUCyxc-1y9HNUOwBDZwhKoeKBSIiV1fgCCQ2_jNi_m2zmLFEyFQWiLMylbLROgQol4KeULMbxJf3RrYva5j7kKrJ3w0xs2CR7Fese5NnPWtO4eyP4O4s8DoZa9DgOxLe4jmr5xGNaZbtxW9iUCRJWmYR9wi1eS4C4b7Yal4Xg62ePz9_fgbIsQu55j2LBZHlwokmIzXH5Ot6jSpbrnZIatdZn-otHRtTZaoXohdIlIwqn2q1EVeBwBLcESOn65u2edDIbL_6s6wdkpl_ytUKOZWB4tAv1AI7EQcaSGgQ-I1GrBhrUsnSsVCc2T-zVOpozofVc6o31Sn3Q'}


    token = event['headers']['Authorization'][7:]
    eventToken = {'token': token}
    claims = jwt.decodejwt(eventToken, None)
    print(claims)
    ownerName = claims['cognito:username']
    print("ownerName", ownerName)

    # # for test:  TODO enable cognito
    # ownerName = "asdf1234"

    print(event)

    body = event['body']
    bodyObject = json.loads(body)
    print(bodyObject)
    groupName= bodyObject['groupName']
    totalSize = bodyObject['totalSize']
    starttimestamp = bodyObject['startTime']
    startTime = datetime.fromtimestamp(starttimestamp)
    restaurantId = bodyObject['restaurantId']
    curTime = datetime.now()

    conn, cursor = connectDb()

    sql = 'use foodieNetDb'
    cursor.execute(sql)
    print('use foodieNetDb ok')

    try:
        # insert into Group
        gid = str(cursor.execute('SELECT UUID_SHORT() from foodieNetDb.Group;'))
        print('new gid', gid)
        print("type(gid)", type(gid))


        search_user_sql = "select * from foodieNetDb.User where username = '{0}';".format(ownerName)
        print(search_user_sql)
        cursor.execute(search_user_sql)
        userInfo = cursor.fetchall()
        userRating = userInfo[0][4]

        if userRating == 0:
            ratingtotal = 0
            ratingtime = 0
        else:
            ratingtotal = userRating
            ratingtime = 1


        insertSQL = "insert into `Group` (gid, groupName,ownerName, \
        totalSize,startTime,rid, ratingtotal, ratingtime, currentGroupCredit, \
        statusChangeTime) values('{0}',\"{1}\", \"{2}\",'{3}'\
        ,'{4}','{5}','{6}','{7}','{8}','{9}')".format(gid,groupName,ownerName, \
        totalSize,startTime,restaurantId,ratingtotal, ratingtime, userRating, curTime)
        print(insertSQL)
        cursor.execute(insertSQL)
        print("Successful insert into Group table!")

        # insert into GroupUser
        insert_g_SQL = "insert into `GroupUser` (gid, username,joinTime\
        ) values('{0}','{1}', '{2}')".format(gid, ownerName, curTime)
        # default not reviewed
        print(insert_g_SQL)
        cursor.execute(insert_g_SQL)
        print("Successful insert into GroupUser table!")


        userInfo = cursor.fetchone()
        conn.commit()
        # conn.close()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"groupId": gid})  # todo: return gid if success
        }
    except:
        conn.rollback()
        # conn.close()
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps("Failed to create the group.")  # todo: return gid if success
        }





    # return {
    #     'statusCode': 200,
    #     'body': json.dumps({"groupId": gid})  # todo: return gid if success
    # }

    # todo: return error code

  
