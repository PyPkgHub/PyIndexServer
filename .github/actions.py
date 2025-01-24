import os
import copy
import re
from bs4 import BeautifulSoup

INDEX_FILE = 'index.html'
TEMPLATE_FILE = 'pkg_template.html'

INDEX_CARD_HTML = '''
<a class="card" href="">
    <span class="package-name">placeholder_name</span>
    <span class="version">placeholder_version</span>
    <br/>
    <span class="description">placeholder_description</span>
</a>'''

def normalize(name):
    """From PEP503: https://www.python.org/dev/peps/pep-0503/"""
    return re.sub(r'[-_.]+', '-', name).lower()

def normalize_version(version):
    version = version.lower()
    return version[1:] if version.startswith('v') else version

def is_stable(version):
    return not ('dev' in version or 'a' in version or 'b' in version or 'rc' in version)

def package_exists(soup, package_name):
    package_ref = f'packages/{package_name}/index.html'
    for anchor in soup.find_all('a', class_='card'):
        if anchor.get('href') == package_ref:
            return True
    return False

def transform_github_url(input_url):
    # Split the input URL to extract relevant information
    parts = input_url.rstrip('/').split('/')
    username, repo = parts[-2], parts[-1]
    
    # Create the raw GitHub content URL
    raw_url = f'https://github.com/{username}/{repo}/blob/main/README.md'
    return raw_url

def update(pkg_name, version, homepage):
    # Read our index first
    with open(INDEX_FILE, encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    
    norm_pkg_name = normalize(pkg_name)
    norm_version = normalize_version(version)

    if not package_exists(soup, norm_pkg_name):
        raise ValueError(f'Package {norm_pkg_name} does not exist')

    # Change the version in the main page (only if stable)
    if is_stable(version):
        anchor = soup.find('a', attrs={'href': f'packages/{norm_pkg_name}/index.html'})
        version_span = anchor.find('span', class_='version')
        version_span.string = norm_version
        
        with open(INDEX_FILE, 'w', encoding='utf-8') as index:
            index.write(soup.prettify())

    # Update the package page
    index_file = f'packages/{norm_pkg_name}/index.html'
    with open(index_file, encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    # Extract the URL from the onclick attribute
    button = soup.find('button', id='repoHomepage')
    if not button:
        raise Exception('Homepage URL not found')

    # Create a new version entry
    versions_section = soup.find('section', class_='versions')
    original_div = versions_section.find_all('div')[-1]
    new_div = copy.copy(original_div)
    
    anchor = new_div.find('a')
    new_div['onclick'] = f'load_readme(\'{version}\', scroll_to_div=true);'
    new_div['id'] = version
    new_div['class'] = 'version-entry'
    
    if not is_stable(version):
        new_div['class'] += ' prerelease'
    else:
        # Update the latest main version
        main_version_span = soup.find('span', id='latest-main-version')
        main_version_span.string = version
        
    anchor.string = norm_version
    anchor['href'] = f'git+{homepage}@{version}#egg={norm_pkg_name}-{norm_version}'
    anchor['class'] = 'version-link'

    # Add the new version entry
    original_div.insert_after(new_div)

    # Save changes
    with open(index_file, 'w', encoding='utf-8') as index:
        index.write(soup.prettify())

def register(pkg_name, version, author, short_desc, homepage):
    link = f'git+{homepage}@{version}'
    long_desc = transform_github_url(homepage)
    
    # Read the index file
    with open(INDEX_FILE, encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    
    norm_pkg_name = normalize(pkg_name)
    norm_version = normalize_version(version)

    if package_exists(soup, norm_pkg_name):
        return update(pkg_name, version, homepage)

    # Create new package card
    placeholder_card = BeautifulSoup(INDEX_CARD_HTML, 'html.parser')
    new_package = placeholder_card.find('a')
    new_package['href'] = f'packages/{norm_pkg_name}/index.html'
    
    # Update package information
    name_span = new_package.find('span', class_='package-name')
    name_span.string = pkg_name
    
    version_span = new_package.find('span', class_='version')
    version_span.string = norm_version
    
    desc_span = new_package.find('span', class_='description')
    desc_span.string = short_desc

    # Add to card container
    card_container = soup.find('div', class_='card-container')
    if not card_container:
        card_container = soup.find('h6', class_='text-header').parent
    
    card_container.append(new_package)

    # Save updated index
    with open(INDEX_FILE, 'w', encoding='utf-8') as index:
        index.write(soup.prettify())

    # Create package page from template
    with open(TEMPLATE_FILE, encoding='utf-8') as temp_file:
        template = temp_file.read()

    # Replace template placeholders
    replacements = {
        '_package_name': pkg_name,
        '_norm_version': norm_version,
        '_version': version,
        '_link': f'{link}#egg={norm_pkg_name}-{norm_version}',
        '_homepage': homepage,
        '_author': author,
        '_long_description': long_desc,
        '_latest_main': version
    }
    
    for key, value in replacements.items():
        template = template.replace(key, value)

    # Create package directory and save package page
    os.makedirs(f'packages/{norm_pkg_name}', exist_ok=True)
    package_index = f'packages/{norm_pkg_name}/index.html'
    with open(package_index, 'w', encoding='utf-8') as f:
        f.write(template)

def delete(pkg_name):
    with open(INDEX_FILE, encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    
    norm_pkg_name = normalize(pkg_name)

    if not package_exists(soup, norm_pkg_name):
        raise ValueError(f'Package {norm_pkg_name} does not exist')

    # Remove package directory and files
    package_dir = f'packages/{norm_pkg_name}'
    if os.path.exists(package_dir):
        import shutil
        shutil.rmtree(package_dir)

    # Remove package card from index
    anchor = soup.find('a', class_='card', attrs={'href': f'packages/{norm_pkg_name}/index.html'})
    if anchor:
        anchor.extract()
        
    with open(INDEX_FILE, 'w', encoding='utf-8') as index:
        index.write(soup.prettify())

def main():
    action = os.environ.get('PKG_ACTION')

    if action == 'REGISTER':
        register(
            pkg_name=os.environ['PKG_NAME'],
            version=os.environ['PKG_VERSION'],
            author=os.environ['PKG_AUTHOR'],
            short_desc=os.environ['PKG_SHORT_DESC'],
            homepage=os.environ['PKG_HOMEPAGE'],
        )
    elif action == 'DELETE':
        delete(pkg_name=os.environ['PKG_NAME'])

if __name__ == '__main__':
    main()