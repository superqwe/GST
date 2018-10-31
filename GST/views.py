from django.http import HttpResponse


def home(request):
    return HttpResponse("""
 <html>
<head>
<title>A web page that points a browser to a different page after 2 seconds</title>
<meta http-equiv="refresh" content="1; URL=/personale/globale">
<meta name="keywords" content="automatic redirection">
</head>
<body>
If your browser doesn't automatically go there within a few seconds, 
you may want to go to 
<a href="/personale/globale">the destination</a> 
manually.
</body>
</html>
    
    """)
