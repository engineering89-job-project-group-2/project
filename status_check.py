import requests

# If website open in browser, test should pass
class Status_check:
    def status_check_home(self):
        check_response= requests.get("http://127.0.0.1:5000/")
        if check_response:
            return True

# Test should fail
    def status_check_upload(self):
        check_response= requests.get("http://127.0.0.1:5000/upload")
        if check_response:
            return True