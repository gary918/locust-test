# Use Locust for Load Testing
## Install Locust
`pip install locust`
## Run Locust with a Single Worker
If you don't need to have a large number of concurren users (>400), you can use single worker by running:
`locust -f locustfile.py`
## Run Locust with Multiple Workers
### Run Locust Master
`locust -f locustfile.py --master`
### Check CPU Resource
* Windows 10: Open Task Manager->Performance to check how many cores does your CPU have. Let's say there are 8 cores.
* MacOS: Open About this Mac -> System Report to check how many cores does your CPU have. Let's say there are 8 cores.
### Run Locust Workers
* Open 8 terminals
* Run `locust -f locustfile.py --worker` in each of the terminals
## Open Browser and Access http://localhost:8089
* Check if you have all workers running
* Input Number of users
* Input Spawn rate (<100)