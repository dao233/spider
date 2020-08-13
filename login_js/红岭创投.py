import execjs

with open('红岭创投.js', 'r', encoding='utf-8') as f:
    hong_js = f.read()

ctx = execjs.compile(hong_js)
print(ctx.call('md5', "123456"))