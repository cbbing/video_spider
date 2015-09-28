# -*- coding: utf8 -*-

import sys

#鎸夌郴缁熷瓧绗﹂泦杈撳嚭(console stdout锛�
def encode_wrap(str):
    try:
        sse = sys.stdout.encoding
        return str.encode(sse)
    except Exception, e:
        return str


def strQ2B(ustring):
    """鍏ㄨ杞崐瑙�"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #鍏ㄨ绌烘牸鐩存帴杞崲
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #鍏ㄨ瀛楃锛堥櫎绌烘牸锛夋牴鎹叧绯昏浆鍖�
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

def strB2Q(ustring):
    """鍗婅杞叏瑙�"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                 #鍗婅绌烘牸鐩存帴杞寲
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        #鍗婅瀛楃锛堥櫎绌烘牸锛夋牴鎹叧绯昏浆鍖�
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring


if __name__ == '__main__':
    b = strQ2B("锝嶏綆[<123abc鍗氬鍥�".decode('cp936'))
    print b

    c = strB2Q("锝嶏綆123abc鍗氬鍥�".decode('cp936'))
    print c