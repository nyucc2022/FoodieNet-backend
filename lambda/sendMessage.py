import pymysql
import json
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

conn, cursor = connectDb()

def lambda_handler(event, context):

    # unpack id token and get username

    # for testing locally you can enter the JWT ID Token here

    # "Bearer eyJraWQiOiIybXlqZ"
    token = event['headers']['Authorization'][7:]
    eventToken = {'token': token}
    claims = jwt.decodejwt(eventToken, None)
    print(claims)

    username = claims['cognito:username']


    print(event)
    body = event['body']
    # {
    #   "groupid": "string",
    #   "message": "string"
    # }
    bodyObject = json.loads(body)
    print(bodyObject)
    groupid = bodyObject['groupId']
    message = bodyObject['message']

    sql = 'use foodieNetDb'
    cursor.execute(sql)
    print('ok')

    insertSQL = "insert into Message (gid,username,message,time) values('{0}','{1}','{2}',now() )".format(groupid,username,message)
    print(insertSQL)
    cursor.execute(insertSQL)
    userInfo = cursor.fetchone()

    conn.commit()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# {
#   "resource":"/sendmessages",
#   "path":"/sendmessages",
#   "httpMethod":"POST",
#   "headers":{
#       "Accept":"*/*",
#       "Accept-Encoding":"gzip, deflate, br",
#       "CloudFront-Forwarded-Proto":"https",
#       "CloudFront-Is-Desktop-Viewer":"true",
#       "CloudFront-Is-Mobile-Viewer":"false",
#       "CloudFront-Is-SmartTV-Viewer":"false",
#       "CloudFront-Is-Tablet-Viewer":"false",
#       "CloudFront-Viewer-Country":"US",
#       "Content-Type":"application/json",
#       "Host":"2da2d0z753.execute-api.us-east-1.amazonaws.com",
#       "Postman-Token":"5d336d94-d8e8-401b-a4bd-4c1eea2847be",
#       "User-Agent":"PostmanRuntime/7.29.0",
#       "Via":"1.1 42f2de9d3efb503e7960e52396f998c8.cloudfront.net (CloudFront)",
#       "X-Amz-Cf-Id":"By6Nzy9elO-PEdTmgNh-cxiTUXj7YAD1PP7rDPJudXwllpilTtkK5Q==",
#       "X-Amzn-Trace-Id":"Root=1-627750db-7ffffaad078f01b1483c2daf",
#       "X-Forwarded-For":"100.8.209.165, 64.252.183.84",
#       "X-Forwarded-Port":"443",
#       "X-Forwarded-Proto":"https"
#   },
#   "multiValueHeaders":{
#       "Accept":[
#          "*/*"
#       ],
#       "Accept-Encoding":[
#          "gzip, deflate, br"
#       ],
#       "CloudFront-Forwarded-Proto":[
#          "https"
#       ],
#       "CloudFront-Is-Desktop-Viewer":[
#          "true"
#       ],
#       "CloudFront-Is-Mobile-Viewer":[
#          "false"
#       ],
#       "CloudFront-Is-SmartTV-Viewer":[
#          "false"
#       ],
#       "CloudFront-Is-Tablet-Viewer":[
#          "false"
#       ],
#       "CloudFront-Viewer-Country":[
#          "US"
#       ],
#       "Content-Type":[
#          "application/json"
#       ],
#       "Host":[
#          "2da2d0z753.execute-api.us-east-1.amazonaws.com"
#       ],
#       "Postman-Token":[
#          "5d336d94-d8e8-401b-a4bd-4c1eea2847be"
#       ],
#       "User-Agent":[
#          "PostmanRuntime/7.29.0"
#       ],
#       "Via":[
#          "1.1 42f2de9d3efb503e7960e52396f998c8.cloudfront.net (CloudFront)"
#       ],
#       "X-Amz-Cf-Id":[
#          "By6Nzy9elO-PEdTmgNh-cxiTUXj7YAD1PP7rDPJudXwllpilTtkK5Q=="
#       ],
#       "X-Amzn-Trace-Id":[
#          "Root=1-627750db-7ffffaad078f01b1483c2daf"
#       ],
#       "X-Forwarded-For":[
#          "100.8.209.165, 64.252.183.84"
#       ],
#       "X-Forwarded-Port":[
#          "443"
#       ],
#       "X-Forwarded-Proto":[
#          "https"
#       ]
#   },
#   "queryStringParameters":"None",
#   "multiValueQueryStringParameters":"None",
#   "pathParameters":"None",
#   "stageVariables":"None",
#   "requestContext":{
#       "resourceId":"x6fwad",
#       "resourcePath":"/sendmessages",
#       "operationName":"addInventory",
#       "httpMethod":"POST",
#       "extendedRequestId":"RymSQFCjoAMFpTw=",
#       "requestTime":"08/May/2022:05:10:51 +0000",
#       "path":"/dev/sendmessages",
#       "accountId":"550667370571",
#       "protocol":"HTTP/1.1",
#       "stage":"dev",
#       "domainPrefix":"2da2d0z753",
#       "requestTimeEpoch":1651986651039,
#       "requestId":"526122f0-e6ef-4919-b91e-708dd73c73a5",
#       "identity":{
#          "cognitoIdentityPoolId":"None",
#          "accountId":"None",
#          "cognitoIdentityId":"None",
#          "caller":"None",
#          "sourceIp":"100.8.209.165",
#          "principalOrgId":"None",
#          "accessKey":"None",
#          "cognitoAuthenticationType":"None",
#          "cognitoAuthenticationProvider":"None",
#          "userArn":"None",
#          "userAgent":"PostmanRuntime/7.29.0",
#          "user":"None"
#       },
#       "domainName":"2da2d0z753.execute-api.us-east-1.amazonaws.com",
#       "apiId":"2da2d0z753"
#   },
#   "body":"{\n    ""groupid"":""groupid"",\n    ""message"":""message""\n}",
#   "isBase64Encoded":false
# }
