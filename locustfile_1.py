#!/usr/bin python3
from locust import between, SequentialTaskSet, HttpUser, task, runners
from random import randrange
import json, logging
 
# Set heartbeat interval to avoid system stop
runners.HEARTBEAT_INTERVAL = 2
 
logger = logging.getLogger(__name__)
data = []
@task(1)
def lookup_transfer(self):       
    global data 
    index = randrange(0, len(data))
    headers = {'content-type': 'application/json', 'Connection': 'close'}    
    with self.client.post("/api/myapi", data=json.dumps(
        {
        "colum1": "someinfo",
        "colum2": data[index],
        "colum3": "someinfo"}),
                                     headers=headers,
                                     name="/api/myapi", catch_response=True) as create_resp:
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
    host = "https://apihost.mycompany.com"
            
    for i in range(5000):
        record_id = i + 1
        craft_id = (i % 250) + 1
        # Only need craft_id,record_id
        data.append({
            "record_id": f"record{record_id}",      
            "craft_id": f"craft{craft_id}",
            "my_value": "102.05"      
            })    