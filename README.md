## Zipkin Tracing Lab

A hands-on lab to explore distributed tracing with Zipkin using a Python client and server.

## Prerequisites

- Python 3.x
- flask
- Docker
- Git

## Setup

## Clone the Repo

```
git clone https://github.com/supertren/zipkin-tracing-lab.git
cd zipkin-tracing-lab
```

## Start Zipkin

```
sudo docker run -d -p 9411:9411 openzipkin/zipkin
```

## Install Dependencies (if necessary)

```
pip install flask requests py_zipkin
```

## Run the Server

```
python src/server.py
```

## Run the Client

```
python src/client.py
```

## View Traces

Open http://localhost:9411 (or http://192.168.1.104:9411 if you are executing the lab on a VM) and click "Find Traces".

## Expected Output

Client:
Trace sent to Zipkin successfully
Response from server: Hello, World!

Server:
Trace sent to Zipkin successfully

## Troubleshooting

Verify Zipkin:

```
docker ps
```

Stop Zipkin dockers:

```
sudo docker stop $(docker ps -q --filter ancestor=openzipkin/zipkin)
```

Restart Zipkin:

```
sudo docker run -d -p 9411:9411 openzipkin/zipkin
```

Open Firewall (if needed):

```
sudo firewall-cmd --add-port=9411/tcp --permanent
sudo firewall-cmd --reload
```

## Contributor

* [Mik Alvarez (supertren)](https://github.com/supertren)

