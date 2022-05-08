
import pymysql
import json

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

    print(event)
    email= event['request']['userAttributes']['email']
    username = event['userName']

    conn, cursor = connectDb()


    sql = 'use foodieNetDb'
    cursor.execute(sql)
    print('ok')

    insertSQL = "insert into `User` (username,email) values('{0}','{1}' )".format(username,email)
    print(insertSQL)
    cursor.execute(insertSQL)
    userInfo = cursor.fetchone()

    conn.commit()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
