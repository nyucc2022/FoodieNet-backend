import pymysql
import json
from datetime import datetime
import jwt

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
    username = claims['cognito:username']

    # username = "asdf1234"

    print(event)

    body = event['body']
    bodyObject = json.loads(body)
    print(bodyObject)
    gid = bodyObject['groupId']
    # print(gid)
    # print("type of gid", type(gid))


    # join group Logic,
    # update info in table Group and GroupUser
    # in Group,
    #     update currentSize, check if == totalSize, change status to 1 and update statusChangeTime
    #     update raingtotal += user's rating, ratingtime += 1, then currentGroupCredit = raingtotal * 0.1 / ratingtime

    # in GroupUser,
    #     check if has joined this group before?
    #     add new user



    curTime = datetime.now()

    # connect to DB
    conn, cursor = connectDb()
    sql = 'use foodieNetDb'
    cursor.execute(sql)
    print('use foodieNetDb ok')

    try:
        search_user_sql = "select * from foodieNetDb.User where username = '{0}';".format(username)
        print(search_user_sql)
        cursor.execute(search_user_sql)
        userInfo = cursor.fetchone()

        print("userInfo", userInfo)
        user_rating = userInfo[4]

        search_group_sql = "select * from foodieNetDb.Group where gid = '{0}';".format(gid)
        print(search_group_sql)
        cursor.execute(search_group_sql)
        groupInfo = cursor.fetchone()

        print("groupInfo", groupInfo)
        g_currentSize = groupInfo[3] + 1  # update currentSize
        g_totalSize = groupInfo[4]
        g_startTimeStamp = groupInfo[5].timestamp()
        g_ratingtotal = groupInfo[7]
        g_ratingtime = groupInfo[8]
        g_currentGroupCredit = groupInfo[9]
        g_status = groupInfo[10]
        g_statusChangeTime = groupInfo[11]


        # todo: check if user has added this group before

        if g_status == 1:
            # conn.close()
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps("Group has filled. Please choose another group!")
            }

        # if has started, the group is treated as expired
        print("g_startTimeStamp: ", g_startTimeStamp)
        curTimeStamp = curTime.timestamp()
        print("currentTimeStamp: ", curTimeStamp)
        print("g_startTimeStamp < curTimeStamp", g_startTimeStamp < curTimeStamp)

        if g_status == 0 and g_startTimeStamp < curTimeStamp:
            # update_group_sql = "UPDATE foodieNetDb.Group SET status='{0}';".format(1)
            # print("update_group_sql", update_group_sql)
            # cursor.execute(update_group_sql)
            # conn.commit()
            # conn.close()
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps("Group has started or has expired. Please choose another group!")
            }


        # update status
        if g_status == 0 and g_currentSize >= g_totalSize:
            # if not complete check size if equals to total change status
            g_status = 1  # set to complete
            g_statusChangeTime = curTime
            # update_group_sql = "UPDATE foodieNetDb.Group SET status='{0}', \
            # statusChangeTime='{1}' WHERE gid='{2}';".format(g_status, g_statusChangeTime, gid)
            # print("update_group_sql", update_group_sql)
            # cursor.execute(update_group_sql)
            # conn.commit()


        # update groupRaing
        g_ratingtotal += user_rating
        g_ratingtime += 1
        g_currentGroupCredit = g_ratingtotal * 0.1 / g_ratingtime
        print("g_currentGroupCredit", g_currentGroupCredit)

        update_group_sql = "UPDATE foodieNetDb.Group SET currentSize='{0}', ratingtotal='{1}', \
        ratingtime='{2}', currentGroupCredit='{3}', status='{4}', \
        statusChangeTime='{5}' WHERE gid='{6}';"\
        .format(g_currentSize, g_ratingtotal, g_ratingtime, g_currentGroupCredit,\
        g_status, g_statusChangeTime, gid)
        print("update_group_sql", update_group_sql)
        cursor.execute(update_group_sql)
        conn.commit()

        # add GroupUser
        insert_group_sql = "insert into `GroupUser` (gid, username,joinTime\
        ) values('{0}','{1}','{2}')".format(gid, username, curTime)
        print(insert_group_sql)
        cursor.execute(insert_group_sql)
        conn.commit()



        # conn.commit()   # update value in a table and commit the changes to the database
        # conn.close()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps("Successfully joined the group.")  # todo: return gid if success
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
            'body': json.dumps("Failed to join the group.")  # todo: return gid if success
        }



  
