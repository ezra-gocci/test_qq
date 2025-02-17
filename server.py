from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import pyodbc 
import boto3
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "rds!db-a5363523-7482-4b8b-9a43-ead46ac89f17"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

    # Your code goes here.
server = 'database-prod.cx0goossu17s.eu-west-2.rds.amazonaws.com'
database = 'master'
username = 'admin'
password = 'Qh[[D#kwV35KeLu8|MV]6S<Y)r$7'
SQL_COPT_SS_TRUST_SERVER_CERTIFICATE = 1228  
SQL_COPT_SS_ENCRYPT = 1223

# Establishing a connection to the SQL Server
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};\
                      SERVER='+server+';\
                      DATABASE='+database+';\
                      UID='+username+';\
                      PWD='+ password, attrs_before={SQL_COPT_SS_ENCRYPT : 1, SQL_COPT_SS_TRUST_SERVER_CERTIFICATE : 1})

cursor = cnxn.cursor()
cursor.execute("CREATE TABLE sample (id INT IDENTITY(1,1) PRIMARY KEY, data NVARCHAR(100))")
result = cursor.execute("SELECT @@version").fetchone()
result = cursor.execute("SELECT* FROM sample").fetchone()

print(result)

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    
