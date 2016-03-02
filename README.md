# telegram 


# installation 
	1. Modify TELEGRAM_TOKEN with your token 
	2. Install python modules:
		```bash
		easy_install python-telegram-bot 
		easy_install gevent
		easy_install flask 
		```
	3. start webserver:
		```bash
		python httpServer.py -d . -i 127.0.0.1
		```
	4. send msg:
		```bash
		curl --data "msg=Hello Web Server" http://127.0.0.1:2001/sendmsg
		```


