import os
import traceback
from collections import deque
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from deep_translator import GoogleTranslator
from googletrans import Translator

SERVICE_URLS = ["https://translate.googleapis.com/$discovery/rest?version=v3", "https://translate.googleapis.com"]

ARTICOL_START = '<!-- ARTICOL START -->'
ARTICOL_END = '<!-- ARTICOL END -->'
SOURCE_PATH = Path('central')
LANG = "hi"  # Hindi
FILE_PATH_QUEUE = deque()
OUTPUT_PATHS = {
    "central": Path("/home/winmorre/Desktop/works/scrape/output")
}
OUTPUT_PATH = Path("output")
EXTENSION_POSTFIX = ".html"

translator = Translator(service_urls=SERVICE_URLS)
google_translator = GoogleTranslator(source="en", target=LANG)


def translation(text: str, lng: str = LANG):
    try:
        trans = translator.translate(text=text, dest=lng).text
    except Exception:
        return text
    return trans


def google_translate(text: str):
    return google_translator.translate(text)


class UnSortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


def get_directory_items(path: Path | None = None):
    if path is not None:
        return sorted(path.iterdir() or SOURCE_PATH.iterdir())
    return sorted(path or SOURCE_PATH.iterdir())


def get_file_name(path):
    file_path = os.path.splitext(path)[0]
    return file_path.split("/")[-1]


def chunk_up_text(text, length):
    return (text[0 + i:length + i] for i in range(0, len(text), length))


def translate_batch(text):
    translated_chunk = google_translator.translate_batch(batch=[chunk for chunk in chunk_up_text(text, 4850)])

    return "".join(translated_chunk)


def recursively_translate(node):
    for x in range(len(node.contents)):
        if isinstance(node.contents[x], str):
            if node.contents[x].strip() != '':
                try:
                    translated_content = translation(node.contents[x])
                    if translated_content is not None:
                        node.contents[x].replaceWith(translated_content)
                except:
                    print(traceback.format_exc())
        elif node.contents[x] is not None:
            recursively_translate(node.contents[x])


def write_new_html_file(soup, file_path):
    with open(file_path, 'w', encoding='utf-8') as new_html:
        new_html.write(soup)
    name = str(file_path).split("/")[-3:]
    print(f"NEW HTML CREATED {'/'.join(name)}")


def make_directory_if_not_exist(path):
    if not path.is_dir:
        return

    if os.path.exists(path):
        return
    else:
        os.mkdir(path)


def translate_html(file_path):
    with open(file_path, mode="r", encoding='utf-8') as html:
        soup = BeautifulSoup(html.read(), 'html.parser')

        try:
            begin_comment = str(soup).index(ARTICOL_START)
            end_comment = str(soup).index(ARTICOL_END)

            for title in soup.findAll('title'):
                recursively_translate(title)

            for meta in soup.findAll('meta'):
                try:
                    meta_content = meta.get('content', None)
                    if meta_content is not None and len(meta_content.split(" ")) > 1 and (
                            'text/html' not in meta_content or 'charset' not in meta_content or \
                            meta_content != 'website' or 'width=device' not in meta_content or \
                            'initial-scale' not in meta_content):
                        trans_content = translation(text=meta_content)
                        meta['content'] = trans_content
                except Exception:
                    print(traceback.format_exc())

            for p in soup.findAll('p'):

                if begin_comment < str(soup).index(str(p)) < end_comment:
                    recursively_translate(p)
            for h1 in soup.findAll('h1'):

                if begin_comment < str(soup).index(str(h1)) < end_comment:
                    recursively_translate(h1)
            for h2 in soup.findAll('h2'):

                if begin_comment < str(soup).index(str(h2)) < end_comment:
                    recursively_translate(h2)

            for h3 in soup.findAll('h3'):

                if begin_comment < str(soup).index(str(h3)) < end_comment:
                    recursively_translate(h3)

            for h4 in soup.findAll('h4'):

                if begin_comment < str(soup).index(str(h4)) < end_comment:
                    recursively_translate(h4)

            for h5 in soup.findAll('h5'):
                # recursively_translate(h5)
                if begin_comment < str(soup).index(str(h5)) < end_comment:
                    recursively_translate(h5)

            for h6 in soup.findAll('h6'):

                if begin_comment < str(soup).index(str(h6)) < end_comment:
                    recursively_translate(h6)

            for label in soup.findAll('label'):

                if begin_comment < str(soup).index(str(label)) < end_comment:  # textarea
                    recursively_translate(label)

            for textarea in soup.findAll('textarea'):

                if begin_comment < str(soup).index(str(textarea)) < end_comment:
                    recursively_translate(textarea)

            for button in soup.findAll('button'):

                if begin_comment < str(soup).index(str(button)) < end_comment:  # title
                    recursively_translate(button)

            for i in soup.findAll('i'):
                if begin_comment < str(soup).index(str(i)) < end_comment:
                    recursively_translate(i)

            for li in soup.findAll('li'):

                if begin_comment < str(soup).index(str(li)) < end_comment:
                    recursively_translate(li)

            for option in soup.findAll('option'):
                if begin_comment < str(soup).index(str(option)) < end_comment:
                    recursively_translate(option)

            for a in soup.findAll('a'):
                # recursively_translate(a)
                if begin_comment < str(soup).index(str(a)) < end_comment:
                    recursively_translate(a)

            for blockquote in soup.findAll('blockquote'):
                # recursively_translate(blockquote)
                if begin_comment < str(soup).index(str(blockquote)) < end_comment:
                    recursively_translate(blockquote)

            for caption in soup.findAll('caption'):
                # recursively_translate(caption)
                if begin_comment < str(soup).index(str(caption)) < end_comment:
                    recursively_translate(caption)

            for legend in soup.findAll('legend'):
                # recursively_translate(legend)
                if begin_comment < str(soup).index(str(legend)) < end_comment:
                    recursively_translate(legend)

            for fieldset in soup.findAll('fieldset'):
                # recursively_translate(fieldset)
                if begin_comment < str(soup).index(str(fieldset)) < end_comment:
                    recursively_translate(fieldset)

            for div in soup.findAll('div'):
                recursively_translate(div)

            for span in soup.findAll('span'):
                # recursively_translate(span)
                if begin_comment < str(soup).index(str(span)) < end_comment:
                    recursively_translate(span)

            for small in soup.findAll('small'):
                # recursively_translate(small)
                if begin_comment < str(soup).index(str(small)) < end_comment:
                    recursively_translate(small)

            for td in soup.findAll('td'):
                # recursively_translate(td)
                if begin_comment < str(soup).index(str(td)) < end_comment:
                    recursively_translate(td)
        except ValueError:
            pass
    return soup


def make_output_dir(path):
    source_part = path.split("central/")[-1]
    dir_name = path.split("/")[-1]
    new_path = OUTPUT_PATH / source_part
    make_directory_if_not_exist(new_path)
    OUTPUT_PATHS[dir_name] = new_path


def translate_in_doc(dir_path):
    paths = get_directory_items(dir_path)
    for path in paths:
        if path.is_dir():
            FILE_PATH_QUEUE.append(path)
        elif str(path).endswith(EXTENSION_POSTFIX):
            translate_file(path)


def translate_file(path):
    soup = translate_html(path)
    soup = soup.encode(formatter=UnSortedAttributes()).decode('utf-8')
    file_name = get_file_name(str(path))
    folder_name = str(path).split("/")[-2]
    folder_path = OUTPUT_PATHS[folder_name]
    new_file_path = folder_path / f"{file_name}.html"
    write_new_html_file(soup, new_file_path)


def run():
    for sub_item in get_directory_items(SOURCE_PATH):
        if str(sub_item).endswith(EXTENSION_POSTFIX) or sub_item.is_dir():
            FILE_PATH_QUEUE.append(sub_item)

    while FILE_PATH_QUEUE:
        sub_path: Path = FILE_PATH_QUEUE.popleft()

        if sub_path.is_dir():
            make_output_dir(str(sub_path))
            translate_in_doc(sub_path)

        elif str(sub_path).endswith(EXTENSION_POSTFIX):
            translate_file(sub_path)


if __name__ == "__main__":
    run()
