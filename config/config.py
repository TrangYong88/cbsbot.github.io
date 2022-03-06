
import argparse

parser = argparse.ArgumentParser(description="Config running params for service")
parser.add_argument("--service-port", dest="service_port", default="5000", help="service port number")
parser.add_argument("--logging-level", dest="logging_level", default="10")
parser.add_argument("--public-host", dest="public_host", default="https://c0d7-113-164-4-6.ngrok.io")
parser.add_argument("--fb-verify-token", dest="fb_verify_token", default="456789")
parser.add_argument("--app-id", dest="app_id", default="654861028899492")
parser.add_argument("--app-secret", dest="app_secret", default="66c6689093c4ed220e04f3b36a32e048")
parser.add_argument("--ssl-certificate", dest="ssl_certificate", default="False")
parser.add_argument("--ssl-certificate-path", dest="ssl_certificate_path", default="/home/ubuntu/docker-service/nginx-selfsigned.crt")
parser.add_argument("--token", dest="token", default="EAAJTl7cBOqQBAOAVisC9wBnRxSoUIgdpbSQXYSAqDTC0saD65mMbexQHuQqdUV032Pp3NuVVzvOIwzABkVEx3zfZA2vlQP2XZCSPdcOhAhDiGOGTmfU7pRkvo7LQGRqQkoQ2r37KN7iXQSEFqLT5FQVKbvIFvZCa3yprxPvqFyZCJhWRnTw5")  # access_token of page
parser.add_argument("--bot-id", dest="bot_id", default="891b5cf0-1533-11ec-9af2-574cd78e0c0c")
parser.add_argument("--page-id", dest="page_id", default="104791705493296")
args = vars(parser.parse_known_args()[0])

service_port = args["service_port"]
logging_level = args["logging_level"]
public_host = args["public_host"]
fb_verify_token = args["fb_verify_token"]
token = args["token"]
app_id = args["app_id"]
app_secret = args["app_secret"]
ssl_certificate = args["ssl_certificate"]
ssl_certificate_path = args["ssl_certificate_path"]
bot_id = args["bot_id"]
page_id = args["page_id"]

