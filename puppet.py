"""Puppet output plugin"""

import os
import sys
import optparse
import re
from lxml import etree, objectify

from pyang import plugin
from pyang import translators
from pyang import statements
from pyang.translators import yin

module_stmts = ['module', 'submodule']
"""Module and submodule statement keywords"""

module_import = ['import', 'include']

yangelement_stmts = ['container', 'list']
"""Keywords of statements that YangElement classes are generated from"""


leaf_stmts = ['leaf', 'leaf-list']
"""Leaf and leaf-list statement keywords"""

def pyang_plugin_init():
    plugin.register_plugin(PuppetPlugin())

class PuppetPlugin(plugin.PyangPlugin):

    def __init__(self):
        self.done = set([])

    def add_output_format(self, fmts):
        self.multiple_modules = False
        fmts['puppet'] = self

        args = sys.argv[1:]
        if not any(x in args for x in ('-f', '--format')):
            if any(x in args for x in ('-d', '--puppet-output')):
                sys.argv.insert(1, '--format')
                sys.argv.insert(2, 'puppet')


    def add_opts(self, optparser):
        """Adds options to pyang, displayed in the pyang CLI help message"""
        optlist = [
            optparse.make_option(
                '-d', '--puppet-output',
                dest='directory',
                help='Generate output to DIRECTORY.')
            ]

        g = optparser.add_option_group('Puppet output specific options')
        g.add_options(optlist)


    def setup_ctx(self, ctx):

        if ctx.opts.format == 'puppet':
            if not ctx.opts.directory:
                ctx.opts.directory = os.getcwd()
        self.ctx = ctx
        pass

    def setup_fmt(self, ctx):
        pass


    def emit(self, ctx, modules, fd):

        module = modules[0]
        root = yang_to_xml(ctx, module)
        ctx.path = os.path.join(ctx.opts.directory , 'puppet_types')

        if not os.path.isdir(ctx.path):
            os.makedirs(ctx.path)

        for module in root.xpath('/t:module', namespaces={'t': yin.yin_namespace}):
            containers = etree.XPath('//t:container',namespaces={'t': yin.yin_namespace})

            for container in containers(module):
                if is_configurable(container):
                    emit_puppet(ctx, module, root, container, fd)

        return

def yang_to_xml(ctx, module):
    body = ''
    temp_fd = open('tmp', 'w')
    translators.yin.emit_yin(ctx, module, temp_fd)
    temp_fd.close()

    for line in open('tmp', 'r').readlines():
        body += line
    os.remove('tmp')
    return etree.fromstring(body)

def ext_module_yang_to_xml(ctx, root, module, yangsearchlist):
    yangextmods = search(root, yangsearchlist)
    extrootlist = []
    for yangextmod in yangextmods:
        extmodule = statements.Statement(module, module, None, 'import', yangextmod.attrib['module'])
        mod = ctx.get_module(extmodule.arg, None)
        extrootlist.append(yang_to_xml(ctx, mod))

    return extrootlist

def is_configurable(element):
    for ele in element.iterchildren():
        if ele.tag == ('{'+yin.yin_namespace+'}'+'config'):
            if 'value' in ele.attrib.keys():
                if ele.attrib['value'] == 'false':
                    return False
    return True

def search(element, tags):
    yangstmts = []
    for ele in element.iterchildren():
        if re.sub('{.*?}', '', ele.tag ) in tags:
            yangstmts.append(ele)
    return yangstmts

def get_resource_name(container,element ):
    path = []
    if 'name' in element.attrib.keys():
        path.append(element.attrib['name'])
    while element != container:
        if 'name' in element.getparent().attrib.keys():
            path.append(element.getparent().attrib['name'])
        element = element.getparent()
    path.reverse()
    return path

def pattern(func):
    def get_pattern(typeelement, fd):
        parent = typeelement.getparent()
        pattern_value = parent.find('{' + yin.yin_namespace + '}' + 'pattern')
        return func (typeelement, fd)
    return get_pattern

def default(func):
    def get_default(typeelement, fd):
        parent = typeelement.getparent()
        default_value = parent.find('{' + yin.yin_namespace + '}' + 'default')
        if default_value is not None:
            fd.write('    defaultto( :' + default_value.attrib['value'] + ' )\n')
        return func(typeelement, fd)
    return get_default

@default
@pattern
def get_string(typeelement, fd):
    pass


@default
def get_unsignedint(typeelement, fd):
    fd.write('    munge { |v| Integer( v ) }\n')


@default
def get_enum(typeelement, fd):
    enumlist = []
    for enum in typeelement.findall('{' + yin.yin_namespace + '}' + 'enum'):
        enumlist.append(enum.attrib['name'])
    fd.write('    newvalues( ' + ', '.join(enumlist) + ' )\n')

@default
def get_boolean(typeelement, fd):
    fd.write('    newvalues( true, false )\n')


yang_types = {
    'enumeration' : get_enum,
    'boolean'     : get_boolean,
    'uint32'      : get_unsignedint,
    'uint64'      : get_unsignedint,
    'string'      : get_string
}

def yangtype_to_puppetvalues(typelist, prefix_dict, typeelement, fd):
    if len(typelist) > 1:
        if typelist[0] in prefix_dict.keys():
            root = prefix_dict[typelist[0]]
            for ele in root.findall('{' + yin.yin_namespace + '}' + 'typedef'):
                if  typelist[1] == ele.attrib['name']:
                    typeelement = ele.find('{' + yin.yin_namespace + '}' + 'type')
                    typeval = typeelement.attrib['name'].split(':')
                    if len(typeval) > 1:
                        yangtype_to_puppetvalues(typeval, prefix_dict, fd)
                    else:
                        try:
                            yang_types[typeelement.attrib['name']](typeelement, fd)
                        except KeyError:
                            pass

    else:
        try:
            yang_types[typeelement.attrib['name']](typeelement, fd)
        except KeyError:
            pass

def create_resource_value(leafstmt, prefix_dict, fd):
    type = []
    for ele in leafstmt.findall('{' + yin.yin_namespace + '}' + 'type'):
        if 'name' in ele.attrib.keys():
            #fd.write('  newvalues( :'+ele.attrib['name']+' )\n')
            typelist = ele.attrib['name'].split(':')

            #Type defination has a prefix
            yangtype_to_puppetvalues(typelist, prefix_dict, ele, fd)


    return

def create_resource_description(element, fd):
    for ele in element.findall('{' + yin.yin_namespace + '}' + 'description'):
        desc = ele.getchildren()[0].text.split('.')[0]
        fd.write('    desc \"'+desc.replace('\n', '')+ '\"\n')
    return


def create_resource_property(yangstmt, prefix_dict, fd):
    keys = []
    for ele in yangstmt.findall('{' + yin.yin_namespace + '}' + 'key'):
        #if re.sub('{.*?}', '', ele.tag ) == 'key':
        if 'value' in ele.attrib.keys():
            keys.append(ele.attrib['value'])

    leafstmts = search(yangstmt, leaf_stmts)
    for leafstmt in leafstmts:
        if is_configurable(leafstmt):
            if 'name' in leafstmt.attrib.keys():
                if leafstmt.attrib['name'] in keys:
                    fd.write('  newparam( :'+leafstmt.attrib['name']+', :namevar=>true ) do\n')
                else:
                    if 'name' in leafstmt.attrib.keys():
                        fd.write('  newproperty( :'+leafstmt.attrib['name']+' ) do\n')

                create_resource_description(leafstmt, fd)
                create_resource_value(leafstmt, prefix_dict, fd)
                fd.write('  end\n\n')

    return

def create_resource_type(container, element, fd):
    path = get_resource_name(container,element )
    typename = '/'.join(path)
    fd.write('Puppet::Type.newtype(:'+typename+ ') do\n')
    fd.write('  @doc = ' + container.xpath('//t:container/t:description/t:text',
                                     namespaces={'t': yin.yin_namespace})[0].text + '\n')
    fd.write('  ensurable\n')
    fd.write('  feature :activable, \"The ability to activate/deactive configuration\"\n\n')

    return


def create_resource_header(container, fd):
    pass

def emit_puppet(ctx, module, root, container, fd):

    importroots = ext_module_yang_to_xml(ctx, root, module, ['import'])
    prefix_dict = {}

    for rootnode in (importroots + [ root ]):
        for module in rootnode.xpath('/t:module', namespaces={'t': yin.yin_namespace}):
            for ele in module.findall('{' + yin.yin_namespace + '}' + 'prefix'):
                #if re.sub('{.*?}', '', ele.tag ) == 'prefix':
                prefix_dict[ele.attrib['value']] = rootnode

    yangstmts = search(container, yangelement_stmts)

    for yangstmt in yangstmts:
        restypename = get_resource_name(container,yangstmt )
        path = os.path.join(ctx.path , 'netdev_' + '_'.join(restypename) + '.rb')
        if os.path.isfile(path):
            os.remove(path)
        fd_res = open(path, 'w+')

        create_resource_header(container, fd_res)
        create_resource_type(container, yangstmt, fd_res)
        create_resource_property(yangstmt, prefix_dict, fd_res)

        fd_res.write('end\n\n')
        fd_res.close()













