import os
from bs4 import BeautifulSoup

for path, dirs, files in os.walk('../'):
    # print path
    # print dirs
    # print files
    parts = path.split('/')
    if '.source' in parts:
        print path
        continue

    for f in files:
        basename, ext = os.path.splitext(f)
        # print basename, ext
        if ext == '.html':
            filepath = os.path.join(path, f)
            with open(filepath, 'r') as fp:
                soup = BeautifulSoup(fp.read(), 'html.parser')

                # delete a.headerlink
                for a in soup.select('a.headerlink'):
                    a.decompose()

                # change css links
                for link in soup.select('link'):
                    if 'rel' in link.attrs:
                        if link.attrs['rel'][0] == 'stylesheet':
                            href = link.attrs['href']
                            link.attrs['href'] = href.replace('_static', 'static')

                # change script links
                for script in soup.select('script'):
                    if 'src' in script.attrs:
                        src = script.attrs['src']
                        script.attrs['src'] = src.replace('_static', 'static')

                # change image referencing
                for img in soup.select('img'):
                    alt = img.attrs['alt']
                    img.attrs['alt'] = alt.replace("_images", "images")
                    src = img.attrs['src']
                    img.attrs['src'] = src.replace("_images", "images")

                # modify matplotlib figures
                for img in soup.select('.figure-plot img'):
                    img.attrs['class'] = ['figure-img', 'img-fluid']
                for p in soup.select('.figure-plot p'):
                    p.decompose()
                for div in soup.select('.figure-plot div.figure'):
                    div.unwrap()

                # figures in general
                for img in soup.select('.figure img'):
                    if 'class' not in img.attrs:
                        img.attrs['class'] = []
                    if 'figure-img' not in img.attrs['class']:
                        img.attrs['class'].append('figure-img')
                    if 'img-fluid' not in img.attrs['class']:
                        img.attrs['class'].append('img-fluid')

                for span in soup.select('.caption-text'):
                    span.unwrap()

                for p in soup.select('p.caption'):
                    p.wrap(soup.new_tag('figcaption'))
                    p.unwrap()

                for div in soup.select('div.figure'):
                    div.wrap(soup.new_tag('figure'))
                    div.unwrap()

                for figure in soup.select('figure'):
                    if 'class' not in figure.attrs:
                        figure.attrs['class'] = []
                    if 'figure' not in figure.attrs['class']:
                        figure.attrs['class'].append('figure')

                for caption in soup.select('figcaption'):
                    if 'class' not in caption.attrs:
                        caption.attrs['class'] = []
                    if 'figure-caption' not in caption.attrs['class']:
                        caption.attrs['class'].append('figure-caption')

                # remove anchored links
                for a in soup.select('.longtable a'):
                    href = a.attrs['href'].split('#')
                    a.attrs['href'] = href[0]

                # add table classes
                for table in soup.select('table'):
                    if 'table' not in table.attrs['class']:
                        table.attrs['class'] += ['table', 'table-responsive', 'table-bordered']

                # add table classes
                for table in soup.select('table.field-list'):
                    if 'table' not in table.attrs['class']:
                        table.attrs['class'] += ['table', 'table-responsive', 'table-bordered']

                # remove unnecessary table classes
                for row in soup.select('tr'):
                    if 'class' in row.attrs:
                        if 'row-odd' in row.attrs['class']:
                            row.attrs['class'].remove('row-odd')
                        if 'row-even' in row.attrs['class']:
                            row.attrs['class'].remove('row-even')

                # # column widths
                # for col in soup.select('col'):
                #     if 'width' in col.attrs:
                #         del col.attrs['width']

                # strip span.pre tags
                for span in soup.select('code .pre'):
                    span.unwrap()

                # link to headers not sections
                for div in soup.select('div.section'):
                    if 'id' in div.attrs:
                        del div.attrs['id']

                # get rid of unnecessary wrappers
                for div in soup.select('div.highlight'):
                    parent = div.parent
                    if 'class' in parent.attrs:
                        if any(c.startswith('highlight') for c in parent.attrs['class']):
                            parent.unwrap()

            with open(filepath, 'w') as fp:
                fp.write(str(soup))
                # fp.write(soup.prettify(formatter='html'))
