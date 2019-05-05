import requests
import urllib3
from .station import stations
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def ticket_inquiry():
    start_station = input("请输入出发站：")
    end_station = input("请输入到达站：")
    date = input("请输入日期：")
    options = input("请输入列车类型（格式g、d、t、k、z）：")
    options = list(options)
    from_station = stations.get(start_station)
    to_station = stations.get(end_station)
    # 构建url
    url = ('https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}'
           '&leftTicketDTO.to_station={}&purpose_codes=ADULT').format(date, from_station, to_station)
    request_value = requests.get(url, verify=False)
    raw_trains = request_value.json()['data']
    TrainCollection(raw_trains, options).pretty_print()


class TrainCollection:
    header = '车次 起始站 到达站 时间 历时 商务座 一等座 二等座 动卧 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合
         available_trains:一个列表，包含可获得的火车班次，每个火车班次是一个字典
         options:查询的选项，如高铁，动车，etc...
        """
        self.available_trains = available_trains
        self.options = options

    @property
    def train(self):
        for item in self.available_trains['result']:
            item = item.split('|')
            train_no = item[3]
            train_p = list(train_no)
            # 获得车次
            # 筛选目标车次
            if not self.options or train_p[0] in self.options:
                start_station = self.available_trains['map'].get(item[6])
                end_station = self.available_trains['map'].get(item[7])
                departure = item[8]
                arrival = item[9]
                duration = item[10]
                business_seat = item[32] or '--'
                first_class_seat = item[31] or '--'
                second_class_seat = item[-4] or '--'
                pneumatic_sleep = item[-3] or '--'
                soft_sleep = item[23] or '--'
                hard_sleep = item[-7] or '--'
                hard_seat = item[-6] or '--'
                no_seat = item[26] or '--'
                row = [train_no, start_station, end_station, departure, arrival, duration, business_seat,
                       first_class_seat, second_class_seat, pneumatic_sleep, soft_sleep, hard_sleep, hard_seat, no_seat]
                yield row

    def pretty_print(self):
        print(self.header)
        for train in self.train:
            print(train)


# if __name__ == '__main__':
#     ticket_inquiry()



