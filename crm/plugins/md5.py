import hashlib


def encryption(*args):
    user = args[0]
    pwd = args[1]
    md5 = hashlib.md5()
    if user and pwd:
        md5.update(user.encode('utf-8'))
        md5.update(pwd.encode('utf-8'))
        new_pwd = md5.hexdigest()
        return new_pwd



if __name__ == '__main__':
    ret = encryption('395798196@qq.com','19931213')
    print(ret)