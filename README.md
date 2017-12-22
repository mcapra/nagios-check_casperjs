# nagios-check_casperjs
A Nagios plugin for executing and validating [CasperJS](http://casperjs.org/) test cases.

```
usage: check_casperjs.py [-h] -p PATH [-w WARNING] [-c CRITICAL] [-a ARGS]
                         [-r] [-b BINARY] [-v]

Executes CasperJS test cases and reports any errors found.

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The logical path to the CasperJS script you want to
                        check.
  -w WARNING, --warning WARNING
                        The warning threshold for the script's execution time
                        (in seconds).
  -c CRITICAL, --critical CRITICAL
                        The critical threshold for the script's execution time
                        (in seconds).
  -a ARGS, --args ARGS  Any arguments you want to pass to your CasperJS
                        script.
  -r, --report          Include a report of each test step in the status
                        output (can be useful for diagnosing failures).
  -b BINARY, --binary BINARY
                        Path to the CasperJS binary you wish to use.
  -v, --verbose         Enable verbose output (this can be VERY long).
```

Examples:
```	
[root@nagiosxi ~]# /tmp/check_casperjs.py -p /tmp/test4.js
OK - PASS 5 tests executed in 1.351s, 5 passed, 0 failed, 0 dubious, 0 skipped.      |runtime=1.351s
[root@nagiosxi ~]# /tmp/check_casperjs.py -p /tmp/test4.js --report
OK - PASS 5 tests executed in 1.386s, 5 passed, 0 failed, 0 dubious, 0 skipped.      (PASS Find an element matching: xpath selector: //*[normalize-space(text())='More information...']) (PASS Find an element matching: xpath selector: //a[normalize-space(text())='More information...']) (PASS Find an element matching: xpath selector: //*[contains(text(), 'Reserved Domains')]) (PASS Find an element matching: p:nth-child(9)) (PASS Find an element matching: div > div) (PASS Resurrectio test) |runtime=1.386s
[root@nagiosxi ~]# /tmp/check_casperjs.py -p /tmp/test4.js
CRITICAL - FAIL 3 tests executed in 6.194s, 2 passed, 1 failed, 0 dubious, 0 skipped.      (FAIL Find an element matching: xpath selector: //*[contains(text(), 'Reserved Domainszz')]) |runtime=6.194s
[root@nagiosxi ~]# /tmp/check_casperjs.py -p /tmp/test4.js --report
CRITICAL - FAIL 3 tests executed in 6.233s, 2 passed, 1 failed, 0 dubious, 0 skipped.      (FAIL Find an element matching: xpath selector: //*[contains(text(), 'Reserved Domainszz')]) |runtime=6.223s
```