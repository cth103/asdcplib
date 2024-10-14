from __future__ import print_function

import subprocess
import shlex
import os
import sys
from waflib import Logs

APPNAME = 'libasdcp-dcpomatic'

if os.path.exists('.git'):
    this_version = subprocess.Popen(shlex.split('git tag -l --points-at HEAD'), stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    last_version = subprocess.Popen(shlex.split('git describe --tags --abbrev=0'), stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    if this_version == '':
        VERSION = '%sdevel' % last_version[1:].strip()
    else:
        VERSION = this_version[1:].strip()
else:
    VERSION = open('VERSION').read().strip()

def options(opt):
    opt.load('compiler_cxx')
    opt.add_option('--target-windows-64', action='store_true', default=False, help='set up to do a cross-compile to Windows 64-bit')
    opt.add_option('--target-windows-32', action='store_true', default=False, help='set up to do a cross-compile to Windows 32-bit')
    opt.add_option('--enable-debug', action='store_true', default=False, help='build with debugging information and without optimisation')
    opt.add_option('--static', action='store_true', default=False, help='build statically')

def configure(conf):
    conf.load('compiler_cxx')
    conf.env.append_value('CXXFLAGS', ['-Wall', '-Wextra', '-D_FILE_OFFSET_BITS=64', '-D__STDC_FORMAT_MACROS'])

    conf.env.TARGET_WINDOWS_64 = conf.options.target_windows_64
    conf.env.TARGET_WINDOWS_32 = conf.options.target_windows_32
    conf.env.TARGET_OSX = sys.platform == 'darwin'
    conf.env.TARGET_LINUX = not conf.env.TARGET_WINDOWS_64 and not conf.env.TARGET_WINDOWS_32 and not conf.env.TARGET_OSX
    conf.env.STATIC = conf.options.static
    conf.env.VERSION = VERSION

    if conf.env.TARGET_OSX:
        conf.env.append_value('CXXFLAGS', ['-Wno-unused-result', '-Wno-unused-parameter', '-Wno-unused-local-typedef'])

    if conf.env.TARGET_LINUX:
        gcc = conf.env['CC_VERSION']
        conf.env.append_value('CXXFLAGS', ['-Wno-unused-result', '-Wno-deprecated-copy', '-Wno-class-memaccess'])

    conf.check_cfg(package='openssl', args='--cflags --libs', uselib_store='OPENSSL', mandatory=True)

    if conf.options.enable_debug:
        conf.env.append_value('CXXFLAGS', '-g')
    else:
        conf.env.append_value('CXXFLAGS', '-O2')

    conf.check(header_name='valgrind/memcheck.h', mandatory=False)

    conf.recurse('src')

def build(bld):
    if bld.env.TARGET_WINDOWS_64:
        flags = '-DKM_WIN32 -DWIN32_LEAN_AND_MEAN -DKM_WIN32_UTF8'
    elif bld.env.TARGET_WINDOWS_32:
        flags = '-DKM_WIN32 -DWIN32_LEAN_AND_MEAN -DKM_WIN32_UTF8'
    else:
        flags = ''

    bld(source='libasdcp-dcpomatic.pc.in',
        version=VERSION,
        includedir='%s/include/libasdcp-dcpomatic' % bld.env.PREFIX,
        libs="-L${libdir} -lasdcp-dcpomatic -lkumu-dcpomatic",
        cflags=flags,
        install_path='${LIBDIR}/pkgconfig')

    bld.recurse('src')

    bld.add_post_fun(post)

def post(ctx):
    if ctx.cmd == 'install':
        ctx.exec_command('/sbin/ldconfig')

def tags(bld):
    os.system('etags src/*.cc src/*.h')

def dist(bld):
    f = open('VERSION', 'w')
    print(VERSION, file=f)
    f.close()
