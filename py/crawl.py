import sys
import os

from html_reader import HTMLReader

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def save_webpage(url, data):
    folder = "htmls"
    os.chdir(folder)
    path = url.split("/")

    for i in range(1, len(path) - 1):
        p = path[i].replace(".", "_")
        folder += "/" + p

        if not os.path.exists(folder):
            os.mkdir(folder)

        os.chdir(folder)

    file = open(p + '.html' if path[-1] != "" else "index.html", "w", encoding="utf-8")
    file.write(data)
    file.close()

pages_links = []

def crawl_web_page(url):
    #url = input("Saisissez l'URL du site web à tracker: ")
    pages_links.append(url)
    links = ""

    for link in pages_links:
        print(link)
        links += link + '\n'
        reader = HTMLReader()
        data = reader.read_url(url)

        page = reader.render()
        if link[-4:-1] == ".png":
            continue

        a_t = page.get_tags("a")

        for t in a_t:
            href = t.get_attr("href")[1]

            if "tel:" in href or "mailto:" in href:
                continue

            hname = href if "http" in href else (link + '/' + href)

            if "#" in hname or "?" in hname:
                continue

            save_webpage(hname, data)

            ne = True

            for l in pages_links:
                if hname == l:
                    ne = False

                    break

            if ne:
                pages_links.append(hname)

    return links
