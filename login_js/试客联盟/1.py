import execjs


with open('1.js', 'r', encoding='utf-8') as f:
    js = f.read()
    ctx = execjs.compile(js)
res = ctx.call('enc', '123456')
print(res)