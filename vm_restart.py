#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:2019-06-22


import pymysql,sys, os,time,datetime,re
reload(sys)
sys.setdefaultencoding('utf-8')
from vm_tool import connect,exec_commands
from vm_tool import Logger,Class_VM
import ConfigParser,codecs
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cf = ConfigParser.ConfigParser()

cf.readfp(codecs.open('config.ini', "r", "utf-8-sig"))

# 连接mysql数据库参数字段
p = Class_VM(cf.get('hj_db', 'db_host'), cf.get('hj_db', 'db_user'), cf.get('hj_db', 'db_pwd'),cf.getint('hj_db', 'db_port'), cf.get('hj_db', 'db'), 'utf8')

# #底层硬重启命令
# cmd = 'xe vm-reboot force=true name-label='
cmd = ['xe vm-start force=true name-label=','xe vm-reboot force=true name-label=']

# 获取教室里面的虚拟机信息
query_vm = '''SELECT  b.vm_name from hj_dg a INNER JOIN hj_vm b on a.id = b.dg_id WHERE b.vm_type = 1 and b.del_flag = 0'''

while True:
        for vmname in p.get_vmname(query_vm):
            # cmd = 'xe vm-shutdown force=true name-label=%s' % (vm_name[vm_id])
            # recmd ='xe vm-reboot force=true name-label=%s' %(vm_name[vm_id])
            vm_status = 'xe vm-list  name-label=%s' %(vmname)
            scmd = 'xe vm-start force=true name-label=%s' % (vmname)
            try:
                #is time restart
                if datetime.datetime.now().strftime('%H:%M') == cf.get('vm_retime', 'set_retime'):

                        # 批量重启虚拟机
                        for vmname in p.get_vmname(query_vm):
                            # cmd = 'xe vm-shutdown force=true name-label=%s' % (vm_name[vm_id])
                            recmd = 'xe vm-reboot force=true name-label=%s' % (vmname)

                            scmd = 'xe vm-start force=true name-label=%s' % (vmname)
                            # ssh1 = connect(host=host[0])
                            result = exec_commands(connect(host=cf.get('xs', 'xs_ip'), username=cf.get('xs', 'xs_acount'),
                                                           password=cf.get('xs', 'xs_pwd')), cmd=recmd)

                            if re.findall(r"halted",result[1],re.M|re.I):
                                exec_commands(connect(host=cf.get('xs', 'xs_ip'), username=cf.get('xs', 'xs_acount'),
                                                      password=cf.get('xs', 'xs_pwd')), cmd=scmd)
                                logger.info(u'{0}正在开机，请等待注册\n'.format(vmname))
                            for i in range(1, int(cf.get('vm_hz', 'vm_hz'))):
                                logger.info(u'现在正在重启{0}请等待注册\n'.format(vmname))
                                time.sleep(1)
                            print u'重启完成'


                #time is not start
                logger.info(u'现在时间%s,还未到才重置时间%s 请等待重置' % (datetime.datetime.now().strftime('%H:%M'), cf.get('vm_retime', 'set_retime')))
                result = exec_commands(connect(host=cf.get('xs','xs_ip'),username=cf.get('xs','xs_acount'),password=cf.get('xs','xs_pwd')),vm_status)
                print result
                # print re.findall(r"halted",result,re.M|re.I)
                if re.findall(r"halted",result[1],re.M|re.I):
                    exec_commands(connect(host=cf.get('xs','xs_ip'),username=cf.get('xs','xs_acount'),password=cf.get('xs','xs_pwd')), scmd)
                    logger.info(u'{0}正在开机，请等待注册\n'.format( vmname))

            except Exception as f:
                         print f,'exec_commands'

            finally:

                        logger.info(unicode("虚拟机名称："+str(vmname),'utf-8'))
                        logger.info(unicode("虚拟机信息："+str(result[1])+str('\n'),'utf-8'))
                        # log.logger.warning('warning')
                        # log.logger.error('error')
                        # log.logger.critical('critical')
                        time.sleep(3)


#
#
