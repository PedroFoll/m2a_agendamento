import datetime
from django.http import HttpResponse
import tempfile
from django.template.loader import render_to_string  
import weasyprint

def export_pdf(request): 
    products = Product.objects.all() # lista todos os produtos 
    html_index = render_to_string('export-pdf.html', {'products': products})  
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='body { font-family: serif} img {margin: 10px; width: 50px;}')]) 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Products'+str(datetime.datetime.now())+'.pdf' 
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush() 
        output.seek(0)
        response.write(output.read()) 
    return response