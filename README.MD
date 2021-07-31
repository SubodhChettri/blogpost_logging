# Get The Basics Right First : Logging

> No code runs faster than **no code**. <br/>
> No code has _**fewer bugs**_ than **no code**. <br/>
> No code uses less memory than **no code**. <br/>
> No code is easier to understand than **no code**. <br/>
> <p align="right">-Mike Perham</p>

## Introduction
Whichever hat you wear within the business, we all hope that it runs smoothly 
with no hiccups at all. The application deployed to the production env is stable
 and works without crashing.
Eventually, the application will crash. Components around it upstream and 
downstream will be impacted. It is always good to be prepared for uncertain 
times for bugs that might creep in.<br/>
Logging and monitoring your complete stack is vital. Logging needs to happen at 
every level of the stack, from the infrastructure to the application hosted on 
it.<br/>
Everyone, to name a few, the product owner, developer or infrastructure 
engineer, must give importance to logging.<br/>
[NIST SP800-92](#ref1) defines logs as "a record of the events occurring within 
an organization’s systems and networks. Logs are composed of log entries; each 
entry contains information related to a specific event that has occurred within 
a system or network."<br/>
Application log entries can be categorized into:<br/>
* Client request and server responses, which can be very helpful in 
  reconstructing sequences of events and determining their apparent outcome. 
* Account information such as successful and failed authentication attempts, 
  account changes (e.g., account creation and deletion, account privilege 
  assignment), and use of privileges.
* Usage information such as the number of transactions occurring in a certain 
  period and the size of transactions.
* Significant operational actions such as application startup and shutdown, 
  application failures, and major application configuration changes. <br/>
The verboseness of log entries needs to be controlled based on the environment 
type. There is no golden rule on the level of details you should log. 
The application log verbosity should be configurable. 
As a rule of thumb, the verboseness 
of an application log should be inversely proportional to the application 
stability. <br/>

<p align="center">
  <img src="/images/loglevel.png">
</p>

<br/>
$$
LogLevel \propto  \frac{1}{ApplicationStability}
$$<br/>

### Sample non production log entries
The verbosity of non production / development environment is kept at the highest level to 
trace all the errors.
```log
2021-07-31 17:43:41,603 - INFO      - log_example.py - main - Call # 3
2021-07-31 17:43:41,603 - INFO      - log_example.py - sum - Arguments: 6, 'c' - Begin function
2021-07-31 17:43:41,603 - INFO      - log_example.py - sum - Adding 2 numbers 6 and c
2021-07-31 17:43:41,603 - ERROR     - log_example.py - sum - Exception: unsupported operand type(s) for +: 'int' and 'str'
2021-07-31 17:43:41,603 - ERROR     - log_example.py - sum - Traceback (most recent call last):
  File "/home/žžžžžžžžžžžžž/repo/blogpost_logging/logger/decorater.py", line 35, in log_decorator_wrapper
    value = func(*args, **kwargs)
  File "log_example.py", line 26, in sum
    return first_number + second_number
TypeError: unsupported operand type(s) for +: 'int' and 'str'

2021-07-31 17:43:41,603 - ERROR     - log_example.py - main - check input data type
2021-07-31 17:43:41,603 - INFO      - log_example.py - main - Call # 3
2021-07-31 17:43:41,603 - INFO      - log_example.py - sum - Arguments: 'd', 10 - Begin function
2021-07-31 17:43:41,603 - INFO      - log_example.py - sum - Adding 2 numbers d and 10
2021-07-31 17:43:41,603 - ERROR     - log_example.py - sum - Exception: can only concatenate str (not "int") to str
2021-07-31 17:43:41,603 - ERROR     - log_example.py - sum - Traceback (most recent call last):
  File "/home/žžžžžžžžžžžžž/repo/blogpost_logging/logger/decorater.py", line 35, in log_decorator_wrapper
    value = func(*args, **kwargs)
  File "log_example.py", line 26, in sum
    return first_number + second_number
TypeError: can only concatenate str (not "int") to str

2021-07-31 17:43:41,603 - ERROR     - log_example.py - main - check input data type
```

### Sample production log entries
Note that I have disable the stack trace in my production logs. This is to avoid 
any underirable data leak through logs [CWE-209](https://cwe.mitre.org/data/definitions/209.html).
This will be a topic for my upcoming article with more details.

```log
2021-07-31 18:21:23,134 - INFO      - log_example.py - main - Call # 1
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Arguments: 5, 6 - Begin function
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Adding 2 numbers 5 and 6
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Returned: - End function 11
2021-07-31 18:21:23,134 - INFO      - log_example.py - main - Call # 2
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Arguments: 'a', 'b' - Begin function
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Adding 2 numbers a and b
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Returned: - End function 'ab'
2021-07-31 18:21:23,134 - INFO      - log_example.py - main - Call # 3
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Arguments: 6, 'c' - Begin function
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Adding 2 numbers 6 and c
2021-07-31 18:21:23,134 - ERROR     - log_example.py - sum - Exception: unsupported operand type(s) for +: 'int' and 'str'
2021-07-31 18:21:23,134 - ERROR     - log_example.py - main - check input data type
2021-07-31 18:21:23,134 - INFO      - log_example.py - main - Call # 3
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Arguments: 'd', 10 - Begin function
2021-07-31 18:21:23,134 - INFO      - log_example.py - sum - Adding 2 numbers d and 10
2021-07-31 18:21:23,134 - ERROR     - log_example.py - sum - Exception: can only concatenate str (not "int") to str
2021-07-31 18:21:23,134 - ERROR     - log_example.py - main - check input data type
```
## Logging made easy
With reference of an [exisiting solution](#ref2) I have cherry picked and 
recreated the decorator. Any function of yours can
have a basic logging by using the [log_decorator](logger/decorater.py)

### Code snippet to decorate your function with logging features
```python
....
@log_decorator(handlers=handlers)
def sum(first_number=1, second_number=2):
    total = first_number + second_number
    return total
....
```
Complete sample solution is located at [sample_log.py](log_example.py)


## Conclusion
Key take way:
* Always log, both successful and unsuccessful events.
* Log enough so you can recreate the timeline of events to trace errors.
* Avoid logging stack traces in production.
* If your application is unstable increase verbosity.
* Use standard logging format so your log analytics tool can use it.

## Reference
1. <a name="ref1">NIST SP800-92</a> https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf
https://csrc.nist.gov/publications/detail/sp/800-92/final
2. <a name="ref2">Referenced log-decorator</a> https://github.com/hima03/log-decorator


licensed under [CC BY 4.0.](http://creativecommons.org/licenses/by/4.0/)