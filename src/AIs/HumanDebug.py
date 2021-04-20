def player_func(x, y):  # for testing manually only
    ##  very important:
#   测试时输入的样例规定:
#    1 2 30
#    1 3 40
#    qaq
#    返回:[(1,2,30.0),(1,3,40.0)]
    result = []
    print('请分行输入操作,三个数用空格隔开,示例：2 5 80 输入任何字母或非法格式以结束输入:')
    try:
        while True:
            inp = list(input().split())
            a = int(inp[0])
            b = int(inp[1])
            c = float(inp[2])
            result.append((a, b, c))
    except Exception:
        print(result)
        return result