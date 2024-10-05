from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException

def check_title(soup, MAX=55):
    tag = soup.title

    if tag and tag.string.strip():
        title = tag.string.strip()
        if len(title) <= MAX:
            return {'status': 'Pass', 'message': 'Valid meta title of good length found.'}
        return {'status': 'Warning', 'message': f'Your title is {len(title)} characters, which exceeds the 55 character limit. The browser will cut off your title.'}
    
    return {'status': 'Fail', 'message': 'No meta title found for this page.'}


def check_meta_description(soup, MAX=155, MIN=70):
    tag = soup.find('meta', attrs={'name': 'description'})

    if tag and tag['content'].strip():
        description = tag['content'].strip()
        if len(description) >= MIN and len(description) <= MAX:
            return {'status': 'Pass', 'message': 'Description is of good length'}
        return {'status': 'Fail', 'message': 'Description is too long'}

    return {'status': 'Fail', 'message': 'No meta description found'}

def check_canonical_link(soup):
    tag = soup.find("link", attrs={"rel": "canonical"})

    if tag and tag['href'].strip():
        canonical_link = tag['href'].strip()
        return {'status': 'Pass', 'message': 'Canonical link found'}
    return {'status': 'Fail', 'message': 'No canonical link found'}

def check_alt_text(soup):
    tags = soup.find_all('img')
    
    missing = 0
    for img in tags:
        if not img.has_attr('alt') or not img['alt'].strip():
            missing += 1
    if missing == 0:
        return {'status': 'Pass', 'message': 'All images have alt text'}
    return {'status': 'Fail', 'message': f'{missing} images are missing alt text'}

def check_robots(url):
    parsed_url = urlparse(url)
    robots = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    try:
        response = requests.get(robots, timeout=5)
        if response.status_code != 200:
            return {'status': 'Fail', 'message': 'No robots.txt found'}
    except RequestException as e:
        return {'status': 'Fail', 'message': 'No robots.txt found'}
    
    robots = response.text.lower()
    missing = list()
    if not ('user-agent' in robots or 'user agent' in robots):
        missing.add('User-agent')
    if not ('sitemap' in robots):
        missing.add('Sitemap')
    if not ('disallow' in robots):
        missing.add('Disallow')
    
    if len(missing) == 0:
        return {'status': 'Pass', 'message': 'Robots.txt is valid'}
    return {'status': 'Fail', 'message': 'robots.txt is missing certain elements'}
'''

def check_favicon(url, soup):
    tag = soup.find('link', rel='shortcut icon')
    if tag is None:
        tag = soup.find('link', rel='icon')
    
    if tag and tag['href']:
        favicon_link = tag['href']
        
        if not favicon_link.startswith('http'):  # relative domain
            favicon_link = url.rstrip('/') + '/' + favicon_link.lstrip('/')
        try:
            response = requests.get(favicon_link, timeout=5)
            if response.status_code == 200:
                return True
            return False
        except RequestException as e:
            return False
    else:
        favicon_link = url.rstrip('/') + '/favicon.ico'
        try:
            response = requests.get(favicon_link, timeout=5)
            if response.status_code == 200:
                return True
            return False
        except RequestException as e:
            return False
'''