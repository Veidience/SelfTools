from urllib.parse import quote

from urllib.parse import unquote


if __name__ == '__main__':
    url = 'https://www.baidu.com/'

    e_url = quote(url)
    print(f'=== URL编码后：{e_url} ===')

    d_url = unquote("http://10.22.196.221:30163/doc.html#/1-default/CMDB%20V2%E7%89%88%E6%9C%AC%E6%8E%A5%E5%8F%A3/knowWalkSearchCiProperty")
    print(f"=== URL解码后：{d_url} ===")