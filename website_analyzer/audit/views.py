from django.shortcuts import render, redirect
from .forms import WebpageForm
import requests
from bs4 import BeautifulSoup
from .checks.seo import *

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = WebpageForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url')
            request.session['submitted_url'] = url
            return redirect('report')
        else:
            return render(request, 'index.html', {'form': form})
    else:
        form = WebpageForm()
    return render(request, 'index.html', {'form': form})

def report(request):
    url = request.session.get('submitted_url', None)
    if not url:
        return redirect('index')
    
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    ######### checks #########
    title_check_result = check_title(soup)
    meta_description_check_result = check_meta_description(soup)
    alt_check_result = check_alt_text(soup)
    robots_check_result = check_robots(url)

    # Create the report dictionary with checks grouped by category
    report = {
        "SEO": {
            "Title Tag": title_check_result,
            "Meta Description": meta_description_check_result,
            "Canonical Link": check_canonical_link(soup),
            "Alt Text for Images": alt_check_result,
            "Robots.txt": robots_check_result
        }
    }

    expanded_categories = [(category, any(check['status'].lower() in ['warning', 'fail'] for check in checks.values())) for category, checks in report.items()]

    # Pass the expanded flags to the template
    return render(request, 'report.html', {
        'url': url,
        'report': report,
        'expanded_categories': expanded_categories,
    })