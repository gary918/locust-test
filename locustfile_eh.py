#!/usr/bin python3
from locust import between, SequentialTaskSet, HttpUser, task, runners
from random import randrange, randint
import json, logging
from datetime import datetime

 
# Set heartbeat interval to avoid system stop
runners.HEARTBEAT_INTERVAL = 2

SERVICE_BUS_NAME_SPACE = "<EVENT_HUBS_SPACE>"
EVENT_HUB_PATH = "<EVENT_HUB_PATH>"
SAS = "<EVENT_HUBS_SAS>"


logger = logging.getLogger(__name__)
data = []
@task(1)
def lookup_transfer(self):       
    global data 
    index = randrange(0, len(data))
    headers = {'content-type': 'application/json', 'Connection': 'close', 'Authorization': SAS}    
    with self.client.post(f"/{EVENT_HUB_PATH}/messages", data=json.dumps(data[index]),
                                     headers=headers,
                                     name="Event Hub", catch_response=True) as create_resp:
        if create_resp.status_code in [200, 201]:
            create_resp.success()
        elif create_resp.status_code == 503:
            logger.info("Invalid host, http status code: {0}".format(create_resp.status_code))
        else:
            create_resp.failure("Unable to create: {0} with http status code: {1}".format(create_resp.text, create_resp.status_code))
        print(f"index = {index}")
 
class TestLargeScale(SequentialTaskSet):
    def on_start(self):
        # Executed per user at the beginning of the test
        pass
 
    tasks = [lookup_transfer]
 
    def on_stop(self):
        # Executed per user at the end of test
        pass
 
class TestLoadTest(HttpUser):
    tasks = [TestLargeScale]
    wait_time = between(5.0, 10.0) 
    host = f"https://{SERVICE_BUS_NAME_SPACE}.servicebus.windows.net"
            
    for i in range(5000):
        data.append({
            "id": randint(1,7),
            "amount": randint(1,20),      
            "ts": str(datetime.now())      
            })