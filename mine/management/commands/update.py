"""
更新订单状态，超过半小时不支付，取消订单，释放内存
"""


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """更新订单状态 回收订单"""

    def add_arguments(self, parser):
        """
        添加命令的参数
        1. 回收所有超时未支付的订单
        python manage.py update --all
        2. 指定回收某一个订单
        python manage.py update --one 20001
        """
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='回收所有超时未支付的订单'
        )

        parser.add_argument(
            '--one',
            action='store',
            dest='one',
            default=False,
            help='指定回收某一个订单'
        )

    def handle(self, *args, **options):
        if options['all']:
            self.stdout.write('开始回收订单')
            # 逻辑处理
            self.stdout.write('---------')
            self.stdout.write('处理完成')
        elif options['one']:
            self.stdout.write('开始回收订单{}'.format(options['one']))
        else:
            self.stderr.write('指令异常')

