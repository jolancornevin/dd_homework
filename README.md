# DataDog Homework by Jolan
This application consume an actively written-to w3c-formatted HTTP access log and then:
- Displays stats every 10s about the traffic during those 10s
- Alerts whenever the total traffic for the past 2 minutes exceeds a certain number on average and alerts when it gets back under the threshold.

## How to
- Run the app: `make run`
- Run the tests: `make test`

## How does it work:
### Technologies
The application is running on Python 3 and a few python dependencies like [clint](https://github.com/kennethreitz/clint), for the command line tools utils and `unittest`, [`coverage`](https://coverage.readthedocs.io/en/v4.5.x/) and [`freezegun`](https://github.com/spulec/freezegun) for testing.

The application also uses the Python 3 type hint feature and check it with [mypy](https://mypy.readthedocs.io/en/latest/index.html).

### Code architecture
The CLI application is organized in one folder, `dd_homework`, and three classes. The `LogAnalyser`, which is responsible for reading the file and creating a `StatData` object, which is going to contains all the useful information we gather about the website traffic. Every 10 seconds, we are going to pass this `StatData` object to the `LogPrinter`, which is responsible for showing the different stats and alert if anything is wrong.

That way, the different logic of parsing the log lines, accumulating data and handling those data to create report and alert are separated concerns and can be changed and extended respectivly.

### Parameters
The CLI application takes three parameters:
- `-t`, `--alert_threshold` which is the threshold to hit before alerting for high traffic.
- `-f`, `--file` which is the file containing your HTTP logs.
- `-l`, `--log_limit` which is the max number of sections we want to show every 10 seconds.

As this is running in Docker, you'll have to update the `ENTRYPOINT ["python", "main.py"]` to specify one or more parameters. If you don't the application will still run with some default values.

## Improving the application design
- We could add a ton of other metrics.
- On the code side, the alerting logic should most likely be de-coupled from the `clint` package. It will enable easier tests and an easier switch of the presentation layer if necessary (like moving it to a web interface).
- On the Devops side, I've made the choice to create a Dockerfile.test file to ease your reviewing process, but in a "real" application, we should obviously move this to a CI tool and automate the test processes.

## Initial Description
***********************************
HTTP log monitoring console program
***********************************

At Datadog, we value working on real solutions to real problems, and as such we think the best way to understand your capabilities is to give you the opportunity to solve a problem similar to the ones we solve on a daily basis. As the next step in our process, we ask that you write a simple console program that monitors HTTP traffic on your machine. Treat this as an opportunity to show us how you would write something you would be proud to put your name on. Feel free to impress us.

- Consume an actively written-to w3c-formatted HTTP access log (https://www.w3.org/Daemon/User/Config/Logging.html). It should default to reading /tmp/access.log and be overrideable
```
Example log lines:
127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123
127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234
127.0.0.1 - frank [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 200 34
127.0.0.1 - mary [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 503 12
```
 - Display stats every 10s about the traffic during those 10s: the sections of the web site with the most hits, as well as interesting summary statistics on the traffic as a whole.
    A section is defined as being what's before the second '/' in the resource section of the log line. For example, the section for "/pages/create" is "/pages"
 - Make sure a user can keep the app running and monitor the log file continuously
 - Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}”. The default threshold should be 10 requests per second, and should be overridable.
 - Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered.
  - Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons.
  - Write a test for the alerting logic.
  - Explain how you’d improve on this application design.
  - If you have access to a linux docker environment, we'd love to be able to docker build and run your project! If you don't though, don't sweat it. As an example for a solution based on python 3:
```
FROM python:3
RUN touch /var/log/access.log  # since the program will read this by default
WORKDIR /usr/src
ADD . /usr/src
ENTRYPOINT ["python", "main.py"]# this is an example for a python program, pick the language of your choice
```
    and we'll have something else write to that log file.


Please submit here:
https://app.greenhouse.io/tests/24114b5dd71384c1fc83798482bd7bae
