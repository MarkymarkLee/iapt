# IAPT

Interactive python development tool

## Goal

### 1. python package

#### Installation

`pip install iapt`

#### How to use

```python
iapt.connect(username: str, password: str, debug=True) # Connect to the server
iapt.send_output(string, should_notify=False) # print output to app and maybe notify user
iapt.progressbar(text, [@iterable]) # something like tqdm
iapt.choices(text, variable_name, choices=[@iterable]) # lets user choose sth as input
iatp.read_input(text, variable_name) # lets user send in inputs
```

### 2. python server

sth like a web server

#### Installation

maybe alot more difficult

#### Use

1.  An api for app
2.  a server for python
3.  should be able to handle many python/app clients

### 3. app

ideally smartphone app in flutter or react web app
