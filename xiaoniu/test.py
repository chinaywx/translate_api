import execjs

# 创建虚拟浏览器环境
# 读取gt4.js文件内容
with open('gt4.js', 'r',encoding='utf8') as file:
    js_code = file.read()

# 创建一个PyExecJS环境
ctx = execjs.compile(js_code, cwd='node_modules')

result =ctx.call("""
initGeetest4({
    captchaId: '93affd0ff28090db468c7fff1741b1f6'
},function (captcha) {
    // captcha为验证码实例
    captcha.appendTo("#captcha");// 调用appendTo将验证码插入到页的某一个元素中，这个元素用户可以自定义
});
""")
# 执行JS代码
# result = ctx.call('initGeetest4', {'captchaId': '93affd0ff28090db468c7fff1741b1f6'})
print(result)
