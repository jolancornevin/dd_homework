# Homework
This application consumes an actively written-to w3c-formatted HTTP access log and then:
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

That way, the different logic of parsing the log lines, accumulating data and handling those data to create report and alert are separated concerns and can be changed and extended respectively.

### Parameters
The CLI application takes three parameters:
- `-t`, `--alert_threshold` which is the threshold to hit before alerting for high traffic.
- `-f`, `--file` which is the file containing your HTTP logs.
- `-l`, `--log_limit` which is the max number of sections we want to show every 10 seconds.

## Improving the application design
- We could add a ton of other metrics.
- On the code side, the alerting logic should most likely be de-coupled from the `clint` package. It will enable easier tests and an easier switch of the presentation layer if necessary (like moving it to a web interface).
- On the Devops side, I've made the choice to create a Dockerfile.test file to ease your reviewing process, but in a "real" application, we should obviously move this to a CI tool and automate the test processes.

## Initial Description
***********************************
HTTP log monitoring console program
***********************************

- Consume an actively written-to w3c-formatted HTTP access log (https://www.w3.org/Daemon/User/Config/Logging.html). It should default to reading /tmp/access.log and be overrideable
```
Example log lines:
127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123
127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234
127.0.0.1 - frank [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 200 34
127.0.0.1 - mary [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 503 12
```
