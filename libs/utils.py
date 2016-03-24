import re

def Html2UBB(content):
    # print content
    
    #以下是将html标签转为ubb标签
    content = content.replace('\r\n', '')
    content = content.replace('\n', '')
    content = content.replace('\t', '')
    content = content.replace('<p><br /></p>', '<br />')
    
    pattern = re.compile( '<img[^>]+src=\"([^\"]+)\"[^>]*>',re.I)
    content = pattern.sub(r'[img]\1[/img]',content)
    pattern = re.compile( '<p[^>]*>([\w\W]+?)</p>',re.I)
    content = pattern.sub(r'\1\r\n',content)
    pattern = re.compile( '<br[^>]*>',re.I)
    content = pattern.sub(r'\r\n',content)

    content = content.replace('&lt;','<')
    content = content.replace('&gt;','>')
    content = content.replace('&nbsp;',' ')
    content = content.replace('&ensp;',' ')
    content = content.replace('&emsp;',' ')
    content = content.replace('&amp;','&')
    content = content.replace('&copy;','©')
    content = content.replace('&reg;','®')

    pattern = re.compile( '<[^>]*?>',re.I)
    content = pattern.sub('',content)
    return content


def parseInt(sin):
    m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
    return int(m.groups()[-1]) if m and not callable(sin) else None

    