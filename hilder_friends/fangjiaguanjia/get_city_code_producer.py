# coding=gbk
import aiohttp
import asyncio
import json
import pika
from lib.log import LogHandler
from pymongo import MongoClient
m = MongoClient(host='192.168.0.136', port=27017)
collection_seaweed = m['fangjia']['seaweed']

n = MongoClient(host='114.80.150.196', port=27777, username='goojia', password='goojia7102')
collection_city_list = n['fangjiaguanjia']['city_list']
log = LogHandler(__name__)


class GuanJiaProducer:

    def __init__(self):
        self.city_dict = {'̨��': 'tz', '����': 'jx', '����': 'nb', '��': 'jh', '����': 'quzhou', '����': 'hz', '����': 'sx',
                          '��ˮ': 'ls', '��ɽ': 'zs', '����': 'huzhou', '����': 'wz', '������': 'hb', '�ں�': 'heihe', '��̨��': 'qth',
                          '����': 'jixi', '���˰���': 'dxal', '��ľ˹': 'jms', '����': 'dq', 'ĵ����': 'mdj', '�绯': 'suihua',
                          '����': 'yichun', '˫Ѽɽ': 'sys', '�������': 'qq', '�׸�': 'hegang', '�Ƹ�': 'yf', '����': 'huizhou',
                          '����': 'zq', 'տ��': 'zj', '����': 'gz', '��Դ': 'heyuan', '����': 'jm', '��β': 'sw', '����': 'sz',
                          '�ع�': 'sg', '�麣': 'zh', '÷��': 'mz', '��ɽ': 'fs', '����': 'yj', '����': 'chaozhou', 'ï��': 'mm',
                          '��ɽ': 'zhongshan', '��Զ': 'qy', '����': 'jy', '��ͷ': 'st', '��ݸ': 'dg', '�ɶ�': 'cd', '��֦��': 'pzh',
                          '����': 'ganzi', '����': 'dazhou', '��ɽ': 'liangshan', '����': 'ab', '����': 'luzhou', '�˱�': 'yb',
                          '����': 'my', 'üɽ': 'ms', '�ϳ�': 'nanchong', '����': 'deyang', '��Ԫ': 'guangyuan', '�Թ�': 'zg',
                          '�㰲': 'ga', '��ɽ': 'leshan', '����': 'bazhong', '�Ű�': 'yaan', '����': 'sn', '����': 'ziyang',
                          '�ڽ�': 'neijiang', '����': 'jz', 'Ӫ��': 'yk', '����': 'dd', '��Ϫ': 'bx', '����': 'liaoyang',
                          '����': 'tieling', '��«��': 'hld', '����': 'dl', '����': 'sy', '�̽�': 'pj', '��ɽ': 'as', '��˳': 'fushun',
                          '����': 'cy', '����': 'fx', '����': 'wuzhou', '����': 'chongzuo', '����': 'yulin', '���Ǹ�': 'fcg',
                          '����': 'qinzhou', '��ɫ': 'baise', '����': 'bh', '����': 'liuzhou', '����': 'gl', '���': 'gg',
                          '����': 'nn', '����': 'hezhou', '�ӳ�': 'hc', '����': 'lb', '����': 'chizhou', 'ͭ��': 'tongling',
                          '����': 'suzhouah', '�ߺ�': 'wuhu', '����': 'bengbu', '����': 'fy', '����': 'xuancheng', '����': 'la',
                          '��ɽ': 'huangshan', '����': 'huaibei', '�Ϸ�': 'hf', '����': 'hn', '����': 'chuzhou', '����': 'bozhou',
                          '����': 'aq', '��ɽ': 'mas', '����': 'hd', '����': 'bd', '��̨': 'xt', '�е�': 'chengde', '��ɽ': 'ts',
                          '�żҿ�': 'zjk', '����': 'cangzhou', '�ȷ�': 'lf', '�ػʵ�': 'qhd', '��ˮ': 'hengshui', 'ʯ��ׯ': 'sj',
                          '����': 'bj', '����': 'cx', '��ɽ': 'ws', '��ͨ': 'zt', '�ն�': 'pe', '����': 'dali', '����': 'diqing',
                          '�º�': 'dh', '��Ϫ': 'yx', '��ɽ': 'bs', '��˫����': 'xsbn', '����': 'km', 'ŭ��': 'nujiang',
                          '�ٲ�': 'lincang', '���': 'honghe', '����': 'qj', '����': 'lj', '����': 'lw', '����': 'rz', '����': 'jn',
                          '��Ӫ': 'dy', '�ĳ�': 'lc', '��ׯ': 'zaozhuang', '����': 'weihai', 'Ϋ��': 'wf', '����': 'linyi',
                          '����': 'heze', '�ൺ': 'qd', '̩��': 'taian', '�Ͳ�': 'zb', '����': 'jining', '����': 'dz', '��̨': 'yt',
                          '����': 'bz', '����': 'ez', '����': 'tm', '����': 'xianning', 'ʮ��': 'shiyan', '����': 'xiantao',
                          '����': 'jingmen', '����': 'suizhou', 'Т��': 'xg', '����': 'xy', '��ʯ': 'hs', '�˲�': 'yichang',
                          '��ũ��': 'snj', '�人': 'wh', '����': 'jingzhou', 'Ǳ��': 'qianjiang', '�Ƹ�': 'hg', '��ʩ': 'es',
                          '�Ͼ�': 'nj', '��Ǩ': 'sq', '̩��': 'taizhoujs', '����': 'xz', '��': 'zhenjiang', '����': 'yz',
                          '����': 'wx', '�γ�': 'yancheng', '����': 'cz', '����': 'su', '���Ƹ�': 'lyg', '����': 'ha', '��ͨ': 'nt',
                          '����': 'jiaozuo', '����': 'kf', '����': 'ny', '����': 'ly', '����': 'xinxiang', '����': 'ay',
                          'פ���': 'zmd', '��Դ': 'jiyuan', 'ƽ��ɽ': 'pds', '����': 'shangqiu', '֣��': 'zz', '���': 'xc',
                          '���': 'py', '�ױ�': 'hebi', '����': 'xinyang', '���': 'lh', '�ܿ�': 'zk', '����Ͽ': 'smx', '����': 'lasa',
                          'ɽ��': 'shannan', '����': 'al', '�տ���': 'rkz', '��֥': 'linzhi', '����': 'changdu', '����': 'nq',
                          '����': 'xa', '����': 'baoji', 'μ��': 'wn', '����': 'ak', '�Ӱ�': 'ya', '����': 'sl', 'ͭ��': 'tc',
                          '����': 'yl', '����': 'hanzhong', '����': 'xianyang', '¤��': 'ln', '����': 'lx', '����': 'gn',
                          '����': 'dx', '���': 'jinchang', '������': 'jyg', '����': 'qingyang', '��Ȫ': 'jq', '����': 'lz',
                          '��ˮ': 'tianshui', '����': 'by', '����': 'ww', '��Ҵ': 'zhangye', 'ƽ��': 'pl', '����': 'shaoyang',
                          '����': 'zhuzhou', '�żҽ�': 'zjj', '����': 'huaihua', '����': 'xx', '����': 'changde', '��ɳ': 'cs',
                          '¦��': 'ld', '����': 'yongzhou', '����': 'hy', '����': 'yy', '����': 'yiyang', '��̶': 'xiangtan',
                          '����': 'chenzhou', '������': 'aks', '����': 'tacheng', '����': 'hm', 'ʯ����': 'shz', '���Ź�': 'tmg',
                          '����': 'yili', '������': 'ale', '����': 'bozhouxj', '����': 'ky', '�����': 'wjq', '����': 'ht',
                          '����̩': 'alt', '��ʲ': 'ks', '����': 'beitun', '��������': 'klmy', '����': 'cj', '˫��': 'shuanghe',
                          '����': 'bazhou', 'ͼľ���': 'tmsk', '����': 'kz', '��³ľ��': 'wl', '��³��': 'tlf', '�ɿ˴���': 'kkdl',
                          '����': 'sm', '��ƽ': 'np', '����': 'fz', '����': 'zhangzhou', '����': 'longyan', 'Ȫ��': 'qz',
                          '����': 'pt', '����': 'xm', '����': 'nd', '����': 'cq', '����': 'zw', '����': 'yc', '��ԭ': 'guyuan',
                          'ʯ��ɽ': 'szs', '����': 'wuzhong', '��ͬ': 'dt', '����': 'jc', '̫ԭ': 'ty', '����': 'changzhi',
                          '����': 'll', '����': 'jinzhong', '����': 'xinzhou', '�ٷ�': 'linfen', '��Ȫ': 'yq', '�˳�': 'yuncheng',
                          '˷��': 'shuozhou', 'ǭ����': 'qdn', 'ͭ��': 'tr', 'ǭ����': 'qxn', '����': 'zy', '����ˮ': 'lps',
                          '��˳': 'anshun', '�Ͻ�': 'bijie', '����': 'gy', 'ǭ��': 'qn', '���ֹ���': 'xlgl', '���': 'cf',
                          '�ں�': 'wuhai', '�˰�': 'xingan', '���ͺ���': 'hh', '�����׶�': 'byne', '������': 'als', 'ͨ��': 'tl',
                          '�����첼': 'wlcb', '���ױ���': 'hlbe', '��ͷ': 'bt', '������˹': 'eds', '��ԭ': 'songyuan', '����': 'cc',
                          '����': 'jl', '��ɽ': 'baishan', '��Դ': 'liaoyuan', 'ͨ��': 'th', '�ӱ�': 'yanbian', '��ƽ': 'sp',
                          '�׳�': 'bc', '�Ϻ�': 'sh', '���': 'tj', '����': 'guoluo', '����': 'huangnan', '����': 'haidong',
                          '����': 'hx', '����': 'haibei', '������': 'hnz', '����': 'ys', '����': 'xn', '�ٸ�': 'lg', '����': 'sanya',
                          '��': 'qh', '����': 'danzhou', '�ֶ�': 'ledong', '����': 'changjiang', '����': 'wanning',
                          '��ɳ': 'baisha', '��ˮ': 'lingshui', '�Ĳ�': 'wc', '����': 'hk', '����': 'qiongzhong', '��ָɽ': 'wzs',
                          '��ɳ': 'ss', '����': 'da', '�Ͳ�': 'tunchang', '��ͤ': 'baoting', '����': 'cm', '����': 'df', 'Ƽ��': 'px',
                          '����': 'sr', '�˴�': 'yichunjx', '����': 'ja', '�ϲ�': 'nc', 'ӥ̶': 'yingtan', '����': 'fuzhou',
                          '������': 'jdz', '�Ž�': 'jj', '����': 'xinyu', '����': 'ganzhou'}
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='114.80.150.196', port=5673, heartbeat=0))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='guanjia')

    def start(self):
        for i in collection_seaweed.find({"status": 0, "cat": "district"}, no_cursor_timeout=True):
            if i['city'] in self.city_dict:
                data = (i['name'], self.city_dict[i['city']])
                self.channel.basic_publish(exchange='',
                                           routing_key='guanjia',
                                           body=json.dumps(data))
                log.info('�Ŷ��� {}'.format(data))


if __name__ == '__main__':
    g = GuanJiaProducer()
    g.start()






