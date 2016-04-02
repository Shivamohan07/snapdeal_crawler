## Snapdeal Crawler

#### Features:
* Option to choose a proxy connection
* Works with authenticated proxy
* Fetches all the reviews of ALL the mobile phones available
* Record logs to capture errors
* Manages directories by itself (Automatic cleaning up of files when execution starts)u

#### Requirements:
* Python 3.4+
* Python modules:
	- bs4
	- requests (v2.9.1+)
	- os
	- re

#### To install the requirements run these commands in the same order:
```shell
$ sudo apt-get install python3
$ sudo apt-get install python3-pip  # Need atleast v8.0.3
```
If `pip3 --version` is <8.0.3. You can get it [here](https://bootstrap.pypa.io/get-pip.py "python pip3") and install it by running `sudo python3 get-pip.py`. Then continue with the remaining installation process.

```shell
$ sudo pip3 install bs4
$ sudo pip3 install requests
$ sudo pip3 install regex
```

### How to run?  
```shell
python3 snapdeal.py #Uses configured python 3+ version available
```
