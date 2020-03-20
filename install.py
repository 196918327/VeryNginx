#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-04 23:48
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : https://github.com/alexazhou/VeryNginx
# @Disc    : install VeryNginx
# @Disc    : support python 2.x and 3.x
import os
import sys
import getopt
import filecmp

work_path = os.getcwd()

    #check if the old version of VeryNginx installed( use upcase directory )
def install_openresty( ):
    yum_install_op = True
    if os.path.exists('/usr/local/openresty') == True:
	print("Seems that a old version of VeryNginx was installed in /usr/local/openresty/...\nBefore install,please remove it and backup the configs if you need.")
        ans = ''
        while ans not in ['y','n']:
            ans = common_input(' Already exists /usr/local/openresty,continue?(y/n)')
        if ans == 'n':
            yum_install_op = False

    #yum安装最新版openresty    
    if yum_install_op == True:
        print('### start install openresty ...')
	exec_sys_cmd('yum install -y yum-utils')
	exec_sys_cmd('yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo')
        exec_sys_cmd('yum clean all')
        exec_sys_cmd('yum makecache')
        exec_sys_cmd('yum install -y openresty')

    else:
        sys.exit(1)

def install_verynginx():
    
    #create user www
    os.system( 'useradd www -s /sbin/nologin -M' )
    #install VeryNginx file
    print('### copy VeryNginx files ...')
    if os.path.exists('/usr/local/openresty') == False:
	exec_sys_cmd( 'mkdir -p /usr/local/openresty' )
    os.chdir( work_path )
    exec_sys_cmd( 'cp -r -f ./verynginx /usr/local/openresty' )
    exec_sys_cmd( 'chown www -R /usr/local/openresty/verynginx' )
    
    #copy nginx config file to openresty
    if os.path.exists('/usr/local/openresty') == True:
       # if filecmp.cmp( '/usr/local/openresty/nginx/conf/nginx.conf', '/usr/local/openresty/nginx/conf/nginx.conf.default', False ) == True:
	print('cp nginx config file to openresty')
	exec_sys_cmd( 'mkdir -p /usr/local/openresty/nginx/conf.d/' )
	exec_sys_cmd( 'mkdir -p /var/log/nginx' )
	exec_sys_cmd( 'cp -f -b ./nginx.conf  /usr/local/openresty/nginx/conf/' )
	exec_sys_cmd( 'cp -f -b ./default.conf  /usr/local/openresty/nginx/conf.d/' )
    else:
        print( 'openresty not found in /usr/local/openresty' )



def update_verynginx():
    install_verynginx()    


def exec_sys_cmd(cmd, accept_failed = False):
    print( cmd )
    ret = os.system( cmd )
    if  ret == 0:
        return ret
    else:
        if accept_failed == False:
            print('*** The installing stopped because something was wrong;')
            exit(1)
        else:
            return False

def common_input( s ):
    if sys.version_info[0] == 3:
        return input( s )
    else:
        return raw_input( s )

def safe_pop(l):
    if len(l) == 0:
        return None
    else:
        return l.pop(0)

def show_help_and_exit():
    help_doc = 'usage: install.py <cmd> <args> ... \n\n\
install cmds and args:\n\
    install\n\
        all (none) :  install verynginx and openresty (default)\n\
        openresty  :  install openresty\n\
        verynginx  :  install verynginx\n\
    update\n\
        verynginx  :  update the installed verynginx\n\
    '
    print(help_doc)
    exit()


if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:], '', []) 
  
    cmd = safe_pop(args)
    if cmd == 'install':
        cmd = safe_pop(args)
        if cmd == 'all' or cmd == None:
            install_openresty()
            install_verynginx()
        elif cmd == 'openresty':
            install_openresty()
        elif cmd == 'verynginx':
            install_verynginx()
        else:
            show_help_and_exit()
    elif cmd == 'update':
        cmd = safe_pop(args)
        if cmd == 'verynginx':
            update_verynginx()
        else:
            show_help_and_exit()
    else:
        show_help_and_exit()
    
    print('*** All finished successfully, enjoy it~')


else:
    print ('install.py had been imported as a module')
    print ('please add group and user www:www')
    print ('to use openresty, systemctl start openresty')
