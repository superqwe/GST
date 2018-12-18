from django.http import HttpResponse


def home(request):
    return HttpResponse("""
 <html>
<head>
<title>Caricamento pagina...</title>
<meta http-equiv="refresh" content="0.1; URL=/personale/completo/in_forza/a">
<meta name="keywords" content="automatic redirection">
</head>
<body>
Se la pagina non è caricata entro alcuni secondi,  
clicca
<a href="/personale/completo/in_forza/a">qui</a> 
.
</body>
</html>
    
    """)
