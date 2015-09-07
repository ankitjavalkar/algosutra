"""
A script that allows the user to download all comic
 issues of a series from <h3110c0m!c.com>
"""

import os
import sys
import re
import urllib.request
import urllib.parse
import concurrent.futures
from bs4 import BeautifulSoup

def get_html_source(url):
    try:
        header = {'User-Agent' : 'Mozilla/5.0'}
        req = urllib.request.Request(url, None, header)
        response = urllib.request.urlopen(req)
        source = response.read()
    except Exception as e:
        print("Error: {0}".format(e))
        return None

    return source

def get_html_div(url, tag, id):
    source = get_html_source(url)
    parent_index = BeautifulSoup(source, 'html.parser')
    div = parent_index.find(tag, id=id)

    return div

def get_paginated_index_links(index_div):
    attr = []
    page_links = []

    pagination = index_div.ul #find('ul', class_='pagination')
    try:
        pagination_item = pagination.find_all('a')
        for item in pagination_item:
            if item['data-page'] not in attr:
                page_links.append(item['href'])
                attr.append(item['data-page'])
    except AttributeError:
        print("Warning: This page probably does not have paginated index")
        return None
    except Exception as e:
        print("Error: {0}".format(e))
        return None

    return page_links

def get_issue_links(div):
    issue_dict = {}

    issue_table_body = div.table.tbody
    link_tag_list = issue_table_body.find_all('a')

    for tag in link_tag_list:
        issue_name = re.sub(r'[^\w]', '', tag.contents[0])
        issue_dict.setdefault(issue_name, tag['href'])

    return issue_dict

def get_pages(link, block):
    pages_dict = {}
    parent_link = link.rsplit('/', 1)[0]

    for option in block.find_all('option'):
        page_id = 'p' + option['value'].strip()
        page_link = os.path.join(parent_link, page_id)
        pages_dict.setdefault(page_id, page_link)
        
    return pages_dict

def get_issue(url):
    issue_dict = {}

    index_div = get_html_div(url, 'div', 'w0')

    index_page_links = get_paginated_index_links(index_div)

    if index_page_links:
        for page in index_page_links:
            index_page_div = get_html_div(url, 'tag', 'w0')
            issue_dict.update(get_issue_links(index_page_div))

    else:
        issue_dict.update(get_issue_links(index_div))

    for issue_no, link in issue_dict.items():
        page_nos_html_list = get_html_div(link, 'select', 'e1')
        if page_nos_html_list:
            pages_dict = get_pages(link, page_nos_html_list)
            os.makedirs(issue_no)
            # os.chdir(destination)
            print(pages_dict)
            header = {'User-Agent' : 'Mozilla/5.0'}
            for pid, link in pages_dict.items():
                page_block = get_html_div(link, 'section', 'main')
                image_link = page_block.img['src']
                parent_link, img_link = (image_link.rsplit('/', 1))
                img_link_clean = urllib.parse.quote(img_link)
                img = get_html_source(os.path.join(parent_link, img_link_clean))
                f = open(pid + '.jpg', 'wb')
                f.write(img)
                f.close()

def main():
    # url = sys.argv[1]
    # with concurrent.futures.ThreadPoolExecutor(max_workers=50) as e:
    #     e.submit(get_issue, url)
    url = sys.argv[1]
    get_issue(url)

if __name__ == '__main__':
    main()