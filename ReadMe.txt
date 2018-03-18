Implementation:--
     Assigned port no as :- 47590 ( Port no :80, asked for priviledge mode during binding with socket)
	 Maintained each server socket with client request in a separate thread.
	 When never Requested resouce is not available,I am sending status code :404 notfound as well as a Header with {Last-Modified :null,Content-Length:0}
     After Suceesfully download in client side.	 I wrote server standard output with time as epoch time.
	 
Sample input and output :---
	   server side ::-
	      make
          python server.py
          host name & port no of HTTP Server ::--remote04: 47500
          /bar.html|128.226.180.165|43874|0.002888
	Clientside:--
	       wget http://remote04.cs.binghamton.edu:47500/bar.html
           --2017-09-19 22:49:23--  http://remote04.cs.binghamton.edu:47500/bar.html
Resolving remote04.cs.binghamton.edu (remote04.cs.binghamton.edu)... 128.226.180.166
Connecting to remote04.cs.binghamton.edu (remote04.cs.binghamton.edu)|128.226.180.166|:47500... connected.
HTTP request sent, awaiting response... 200 No headers, assuming HTTP/0.9
Length: unspecified
Saving to: ‘bar.html.8’


Content in bar.html.8:-----
    
HTTP/1.1 200 OK
Date : Tue, 19 Sep 2017 22:49:23
Server : :Multi-threaded HTTP server
Last-Modified :Tue, 19 Sep 2017 18:25:27
Content-Type :text/html
Content-Length :162

<html>
<head>
<title>
A Simple HTML Document
</title>
</head>
<body>
<p>This is a very simple HTML document</p>
<p>It only has two paragraphs</p>
</body>
</html>r

