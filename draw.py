import csv
import matplotlib.pyplot as plt

def draw():
    # 读取爬到的数据，对各个地区进行计算高校总数
    nums = {}
    with open("data.csv", 'r') as f:
        csv_reader = csv.reader(f)
        next(f, None)
        for line in csv_reader:
            if line[1] in nums:
                nums[line[1]] += 1
            else:
                nums[line[1]] = 1

    # 写入csv文件，将字典存入列表
    list = sorted(nums.items(), key=lambda item: item[1], reverse=True)
    locals = []
    counts = []
    with open("count.csv", 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['local', 'count'])
    for i in list:
        locals.append(i[0])
        counts.append(i[1])
        with open("count.csv", 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([i[0], i[1]])

    # 对结果进行可视化操作
    params = {
        'figure.figsize': '15, 10'
    }
    plt.rcParams.update(params)
    rects = plt.bar(range(len(counts)), counts, tick_label=locals)
    for rect in rects:
        x = rect.get_x()
        height = rect.get_height()
        plt.text(x + 0.2, 1.01 * height, str(height))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.savefig('data.jpg')
    plt.show()


def __main__():
    draw()
