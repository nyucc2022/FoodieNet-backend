import json
import pymysql
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

conn, cursor = connectDb()


# todo: close the connection

def get_groupInfo_gid(gid):
    search_group_sql = "select * from foodieNetDb.Group where gid = '{0}';".format(gid)
    print(search_group_sql)
    cursor.execute(search_group_sql)
    groupInfo = cursor.fetchall()
    # since gid is uniq, should get only one info
    print("get_groupInfo_gid: groupInfo", groupInfo)
    return groupInfo


def get_restInfo(rid):
    search_res_sql = "select * from foodieNetDb.Restaurant where rid = '{0}';".format(rid)
    print(search_res_sql)
    cursor.execute(search_res_sql)
    resInfo = cursor.fetchall()
    ret_restaurantInfo = {
        "name": resInfo[0][1],
        "cuisine": resInfo[0][2],
        "address": resInfo[0][3],
        "zipcode": resInfo[0][4],
        "longitude": resInfo[0][5],
        "latitude": resInfo[0][6],
        "image": resInfo[0][7]
    }
    return ret_restaurantInfo


def get_reviewedUserList(gid):
    # todo: only for test, set Reviewed to 0
    search_reviewedGroupUser_sql = "select * from foodieNetDb.GroupUser where gid = '{0}' and Reviewed = 1;".format(gid)
    print(search_reviewedGroupUser_sql)
    cursor.execute(search_reviewedGroupUser_sql)
    reviewedGroupUserInfo = cursor.fetchall()
    # TODO: check if it's a list??? should be
    reviewedGroupUsernameList = reviewedGroupUserInfo
    print(type(reviewedGroupUsernameList))
    print("reviewedGroupUsernameList", reviewedGroupUsernameList)
    # reviewedUserList = reviewedGroupUsernameList

    reviewedUserList = []
    for i in range(len(reviewedGroupUsernameList)):
        reviewedUserList.append(reviewedGroupUsernameList[i][1])
    return reviewedUserList


def get_groupUsernameList(gid):
    search_groupUser_sql = "select * from foodieNetDb.GroupUser where gid = '{0}';".format(gid)
    print(search_groupUser_sql)
    cursor.execute(search_groupUser_sql)
    groupUserInfo = cursor.fetchall()
    # TODO: check if it's a list??? should be
    groupUsernameList = []
    for i in range(len(groupUserInfo)):
        groupUsernameList.append(groupUserInfo[i][1])
    return groupUsernameList


def get_retRes(groupInfo):
    results = []
    for i in range(len(groupInfo)):
        gid = groupInfo[i][0]
        rid = groupInfo[i][6]
        ret_restaurantInfo = get_restInfo(rid)
        reviewedUserList = get_reviewedUserList(gid)
        groupUsernameList = get_groupUsernameList(gid)
        ret_single = {
            "groupId": gid,
            "groupName": groupInfo[i][1],
            "ownerName": groupInfo[i][2],
            "currentSize": groupInfo[i][3],
            "totalSize": groupInfo[i][4],
            "startTime": groupInfo[i][5].timestamp(),
            "restaurant": ret_restaurantInfo,
            "reviewedUserList": reviewedUserList,
            "groupUsernameList": groupUsernameList,
            "currentGroupCredit": groupInfo[i][9],
            "status": groupInfo[i][10],
            "statusChangeTime": groupInfo[i][11].timestamp()
        }
        results.append(ret_single)
    return results

def listToSQLString(s):
    str1 = "("
    # traverse in the string
    for ele in s:
        str1 += "\""
        str1 += ele
        str1 += "\","
    return str1

def lambda_handler(event, context):
    print(event)

    token = event['headers']['Authorization'][7:]
    eventToken = {'token': token}
    claims = jwt.decodejwt(eventToken, None)
    print(claims)
    username = claims['cognito:username']

    # # # for test
    # username = "asdf1234"

    sql = 'use foodieNetDb'
    cursor.execute(sql)
    print('use foodieNetDb ok')

    body = event['body']
    bodyObject = json.loads(body)
    print(bodyObject)
    # get user info from User

    curTime = datetime.now()
    curTimeStamp = curTime.timestamp()

    results = []

    if not (bodyObject.get('groupId') is None):
        # if groupId exists, return info of this group
        gid = bodyObject['groupId']
        groupInfo = get_groupInfo_gid(gid)
        print("groupInfo", groupInfo)

        # get res info from table Restaurant where rid =
        # rid = groupInfo[0][6]
        # ret_restaurantInfo = get_restInfo(rid)

        # get all username from table GroupUser where gid = 'gid' and Reviewed = 1
        # reviewedUserList = get_reviewedUserList(gid)

        # get all username from table GroupUser where gid =
        # groupUsernameList = get_groupUsernameList(gid)

        results = get_retRes(groupInfo)
        print("results", results)
        conn.commit()
        # conn.close()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(results)
        }

    elif not (bodyObject.get('myGroupFlag') is None):
        myGroupFlag = bodyObject['myGroupFlag']
        if myGroupFlag:
            print("search my groups")
            # if myGroupFlag is true, return all the groups where ownerName="my_username"
            print(username)
            search_group_sql = "select * from foodieNetDb.GroupUser where username = '{0}';".format(username)
            print(search_group_sql)
            cursor.execute(search_group_sql)
            groupUserInfo = cursor.fetchall()
            # since gid is uniq, should get only one info
            print("groupUserInfo", groupUserInfo)
            groupInfo = []
            for i in range(len(groupUserInfo)):
                curGid = groupUserInfo[i][0]
                groupInfo.append(list(get_groupInfo_gid(curGid)[0]))
            results = get_retRes(groupInfo)
            print("results", results)
            conn.commit()
            # conn.close()
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(results)
            }


    else:
        sizeRange = bodyObject['sizeRange']
        cuisineTypeList = bodyObject['cuisineTypeList']
        groupCreditRange = bodyObject['groupCreditRange']
        name = bodyObject['name']

        # TODO:  and startTime > {0}".format(curTime)

        search_qrl = "select * from foodieNetDb.Group g, foodieNetDb.Restaurant r \
        where g.status=0 and g.totalSize >= {0} and g.totalSize <= {1} and \
        g.currentGroupCredit >= {2} and g.currentGroupCredit <= {3} \
        and r.rid=g.rid and r.name like(\"%{4}%\")"\
        .format(sizeRange[0], sizeRange[1], groupCreditRange[0], groupCreditRange[1], name);


        if len(cuisineTypeList) != 0:
            cuisineStr = listToSQLString(cuisineTypeList)[:-1]+")"
            search_qrl += " and r.cuisine in {0}".format(cuisineStr);

        cursor.execute(search_qrl)
        print(search_qrl)


        # search_group_sql = "select * from foodieNetDb.Group where status=0 and startTime > \"{0}\"".format(curTime)
        # print(search_group_sql)
        # cursor.execute(search_group_sql)
        groupInfo = cursor.fetchall()
        # since gid is uniq, should get only one info
        print("groupInfo", groupInfo)

        results = get_retRes(groupInfo)
        print("results", results)
        conn.commit()
        # conn.close()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(results)
        }


# TODO: return 400 error?? when??
