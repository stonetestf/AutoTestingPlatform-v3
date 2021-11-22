import random
import string


class Common(object):
    # 生成随机值
    def generate_random_value(self):
        new_password = ""
        count = 4
        src_digits = string.digits  # string_数字
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母

        for index, item in enumerate(range(count), 1):
            # 随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
            digits_num = random.randint(1, 6)
            uppercase_num = random.randint(1, 8 - digits_num - 1)
            lowercase_num = 8 - (digits_num + uppercase_num)

            # 生成字符串
            password = random.sample(src_digits, digits_num) + random.sample(src_uppercase,
                                                                             uppercase_num) + random.sample(
                src_lowercase, lowercase_num)
            # 打乱字符串
            random.shuffle(password)
            # 列表转字符串
            if count - index != 0:
                new_password += ''.join(password) + "-"
            else:
                new_password += ''.join(password)
            # print(new_password)

        return new_password

    # 转换POST请求来时list转换问题
    def conversion_post_lists(self,listName,listData):
        """
        :param listName: 需要转换的list名称
        :param listData:
        :return:
        """
        lists = []
        indexLists = []
        for i in listData:
            if i.startswith(listName):
                index = int(i.split('[')[1].replace(']', ''))
                indexLists.append(index)

        for i in set(indexLists):
            itemDicts = {}
            for item in listData:
                if item.startswith(listName):
                    keyName = item.split('[')[-1].replace(']', '')
                    itemDicts[keyName] = listData[f"fileList[{i}][{keyName}]"]
            lists.append(itemDicts)
        return lists
