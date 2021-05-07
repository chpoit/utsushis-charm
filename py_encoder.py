__all__ = ['py_encoder']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['ob', 'Bb', 'H', 'pb', 'kb', 'ib', 'G', 'fa', 'EncodedCharmHolder', 'weirdifyCharms', '_createClass', 'qb', 'convertToUint', 'Ob', 'btoa_func', 'sb', 'saveEncodedCharms', 'wb', '_classCallCheck', 'loadCharmFromLoadedJsonString', 'encodeFromPython', 'L', 'Tb', 'compressUintMaybe', 'BufferTypeThing', 'mb', 'K', 'E', 'encodeCharmListIntoFirstVar', 'rb', 'lb', 'Cb', 'encodeCharms', 'tb', 'main', '_typeof', 'jb', 'getPadThing', 'generateNoisyFirstChar', 'Qb', 'loadCharmsFromFile'])
@Js
def PyJsHoisted__classCallCheck_(instance, Constructor, this, arguments, var=var):
    var = Scope({'instance':instance, 'Constructor':Constructor, 'this':this, 'arguments':arguments}, var)
    var.registers(['Constructor', 'instance'])
    if var.get('instance').instanceof(var.get('Constructor')).neg():
        PyJsTempException = JsToPyException(var.get('TypeError').create(Js('Cannot call a class as a function')))
        raise PyJsTempException
PyJsHoisted__classCallCheck_.func_name = '_classCallCheck'
var.put('_classCallCheck', PyJsHoisted__classCallCheck_)
@Js
def PyJsHoisted_L_(a, b, c, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    var.get('wb')(var.get('a'), var.get('b'), var.get('c'))
    var.put('b', var.get('a').get('a').get(var.get('c')))
    ((var.get('b')==var.get('qb')) and var.put('b', var.get('a').get('a').put(var.get('c'), Js([]))))
    return var.get('b')
PyJsHoisted_L_.func_name = 'L'
var.put('L', PyJsHoisted_L_)
@Js
def PyJsHoisted_wb_(a, b, c, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'e', 'b', 'd', 'f'])
    (var.get('a').get('a') or var.get('a').put('a', Js({})))
    if var.get('a').get('a').get(var.get('c')).neg():
        #for JS loop
        var.put('d', var.get('G')(var.get('a'), var.get('c')))
        var.put('e', Js([]))
        var.put('f', Js(0.0))
        while (var.get('f')<var.get('d').get('length')):
            try:
                var.get('e').put(var.get('f'), var.get('b').create(var.get('d').get(var.get('f'))))
            finally:
                    (var.put('f',Js(var.get('f').to_number())+Js(1))-Js(1))
        var.get('a').get('a').put(var.get('c'), var.get('e'))
PyJsHoisted_wb_.func_name = 'wb'
var.put('wb', PyJsHoisted_wb_)
@Js
def PyJsHoisted_G_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    if (var.get('b')<var.get('a').get('f')):
        var.put('b', var.get('a').get('c'), '+')
        var.put('c', var.get('a').get('F').get(var.get('b')))
        return (var.get('a').get('F').put(var.get('b'), Js([])) if PyJsStrictEq(var.get('c'),var.get('qb')) else var.get('c'))
    if var.get('a').get('b'):
        return PyJsComma(var.put('c', var.get('a').get('b').get(var.get('b'))),(var.get('a').get('b').put(var.get('b'), Js([])) if PyJsStrictEq(var.get('c'),var.get('qb')) else var.get('c')))
PyJsHoisted_G_.func_name = 'G'
var.put('G', PyJsHoisted_G_)
@Js
def PyJsHoisted_H_(a, b, c, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    var.put('a', var.get('G')(var.get('a'), var.get('b')))
    return (var.get('c') if (var.get(u"null")==var.get('a')) else var.get('a'))
PyJsHoisted_H_.func_name = 'H'
var.put('H', PyJsHoisted_H_)
@Js
def PyJsHoisted_fa_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    var.put('b', (Js('undefined') if PyJsStrictEq(var.get('a',throw=False).typeof(),Js('undefined')) else var.get('_typeof')(var.get('a'))))
    if (Js('object')==var.get('b')):
        if var.get('a'):
            if var.get('a').instanceof(var.get('Array')):
                return Js('array')
            if var.get('a').instanceof(var.get('Object')):
                return var.get('b')
            var.put('c', var.get('Object').get('prototype').get('toString').callprop('call', var.get('a')))
            if (Js('[object Window]')==var.get('c')):
                return Js('object')
            if ((Js('[object Array]')==var.get('c')) or ((((Js('number')==var.get('a').get('length').typeof()) and (Js('undefined')!=var.get('a').get('splice').typeof())) and (Js('undefined')!=var.get('a').get('propertyIsEnumerable').typeof())) and var.get('a').callprop('propertyIsEnumerable', Js('splice')).neg())):
                return Js('array')
            if ((Js('[object Function]')==var.get('c')) or (((Js('undefined')!=var.get('a').get('call').typeof()) and (Js('undefined')!=var.get('a').get('propertyIsEnumerable').typeof())) and var.get('a').callprop('propertyIsEnumerable', Js('call')).neg())):
                return Js('function')
        else:
            return Js('null')
    else:
        if ((Js('function')==var.get('b')) and (Js('undefined')==var.get('a').get('call').typeof())):
            return Js('object')
    return var.get('b')
PyJsHoisted_fa_.func_name = 'fa'
var.put('fa', PyJsHoisted_fa_)
@Js
def PyJsHoisted_rb_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'b'])
    var.put('b', (var.get('a').get('f')+var.get('a').get('c')))
    (var.get('a').get('F').get(var.get('b')) or var.get('a').put('b', var.get('a').get('F').put(var.get('b'), Js({}))))
PyJsHoisted_rb_.func_name = 'rb'
var.put('rb', PyJsHoisted_rb_)
@Js
def PyJsHoisted_tb_(a, b, c, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    (var.get('a').get('F').put((var.get('b')+var.get('a').get('c')), var.get('c')) if (var.get('b')<var.get('a').get('f')) else PyJsComma(var.get('rb')(var.get('a')),var.get('a').get('b').put(var.get('b'), var.get('c'))))
PyJsHoisted_tb_.func_name = 'tb'
var.put('tb', PyJsHoisted_tb_)
@Js
def PyJsHoisted_sb_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'e', 'b', 'd', 'h', 'f'])
    #for JS loop
    var.put('e', Js(0.0))
    while (var.get('e')<var.get('b').get('length')):
        try:
            var.put('f', var.get('b').get(var.get('e')))
            var.put('h', var.get('G')(var.get('a'), var.get('f')))
            ((var.get(u"null")!=var.get('h')) and PyJsComma(PyJsComma(var.put('c', var.get('f')),var.put('d', var.get('h'))),var.get('tb')(var.get('a'), var.get('f'), PyJsComma(Js(0.0), Js(None)))))
        finally:
                (var.put('e',Js(var.get('e').to_number())+Js(1))-Js(1))
    return (PyJsComma(var.get('tb')(var.get('a'), var.get('c'), var.get('d')),var.get('c')) if var.get('c') else Js(0.0))
PyJsHoisted_sb_.func_name = 'sb'
var.put('sb', PyJsHoisted_sb_)
@Js
def PyJsHoisted_pb_(a, b, c, d, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'd':d, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'e', 'b', 'd'])
    var.get('a').put('a', var.get(u"null"))
    (var.get('b') or var.put('b', Js([])))
    var.get('a').put('j', PyJsComma(Js(0.0), Js(None)))
    var.get('a').put('c', (-Js(1.0)))
    var.get('a').put('F', var.get('b'))
    class JS_BREAK_LABEL_61(Exception): pass
    try:
        if var.put('b', var.get('a').get('F').get('length')):
            var.put('b',Js(var.get('b').to_number())-Js(1))
            var.put('e', var.get('a').get('F').get(var.get('b')))
            if (((PyJsStrictEq(var.get(u"null"),var.get('e')) or (Js('object')!=(Js('undefined') if PyJsStrictEq(var.get('e',throw=False).typeof(),Js('undefined')) else var.get('_typeof')(var.get('e'))))) or (Js('array')==var.get('fa')(var.get('e')))) or (var.get('ob') and var.get('e').instanceof(var.get('Uint8Array')))).neg():
                var.get('a').put('f', (var.get('b')-var.get('a').get('c')))
                var.get('a').put('b', var.get('e'))
                raise JS_BREAK_LABEL_61("Breaked")
        var.get('a').put('f', var.get('Number').get('MAX_VALUE'))
    except JS_BREAK_LABEL_61:
        pass
    var.get('a').put('i', Js({}))
    if var.get('c'):
        #for JS loop
        var.put('b', Js(0.0))
        while (var.get('b')<var.get('c').get('length')):
            try:
                PyJsComma(var.put('e', var.get('c').get(var.get('b'))),(PyJsComma(var.put('e', var.get('a').get('c'), '+'),var.get('a').get('F').put(var.get('e'), (var.get('a').get('F').get(var.get('e')) or var.get('qb')))) if (var.get('e')<var.get('a').get('f')) else PyJsComma(var.get('rb')(var.get('a')),var.get('a').get('b').put(var.get('e'), (var.get('a').get('b').get(var.get('e')) or var.get('qb'))))))
            finally:
                    (var.put('b',Js(var.get('b').to_number())+Js(1))-Js(1))
    if (var.get('d') and var.get('d').get('length')):
        #for JS loop
        var.put('b', Js(0.0))
        while (var.get('b')<var.get('d').get('length')):
            try:
                var.get('sb')(var.get('a'), var.get('d').get(var.get('b')))
            finally:
                    (var.put('b',Js(var.get('b').to_number())+Js(1))-Js(1))
PyJsHoisted_pb_.func_name = 'pb'
var.put('pb', PyJsHoisted_pb_)
@Js
def PyJsHoisted_getPadThing_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'b'])
    var.put('b', var.get('a').get('a'))
    var.get('a').put('a', Js([]))
    return var.get('b')
PyJsHoisted_getPadThing_.func_name = 'getPadThing'
var.put('getPadThing', PyJsHoisted_getPadThing_)
@Js
def PyJsHoisted_generateNoisyFirstChar_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'b'])
    #for JS loop
    
    while (Js(127.0)<var.get('b')):
        PyJsComma(var.get('a').get('a').callprop('push', ((var.get('b')&Js(127.0))|Js(128.0))),var.put('b', Js(7.0), '>>>'))
    
    var.get('a').get('a').callprop('push', var.get('b'))
PyJsHoisted_generateNoisyFirstChar_.func_name = 'generateNoisyFirstChar'
var.put('generateNoisyFirstChar', PyJsHoisted_generateNoisyFirstChar_)
@Js
def PyJsHoisted_kb_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    var.put('c', var.get('b').callprop('pop'))
    #for JS loop
    var.put('c', ((var.get('a').get('b')+var.get('a').get('a').callprop('length'))-var.get('c')))
    while (Js(127.0)<var.get('c')):
        PyJsComma(PyJsComma(var.get('b').callprop('push', ((var.get('c')&Js(127.0))|Js(128.0))),var.put('c', Js(7.0), '>>>')),(var.get('a').put('b',Js(var.get('a').get('b').to_number())+Js(1))-Js(1)))
    
    var.get('b').callprop('push', var.get('c'))
    (var.get('a').put('b',Js(var.get('a').get('b').to_number())+Js(1))-Js(1))
PyJsHoisted_kb_.func_name = 'kb'
var.put('kb', PyJsHoisted_kb_)
@Js
def PyJsHoisted_jb_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'b'])
    var.get('generateNoisyFirstChar')(var.get('a').get('a'), ((Js(8.0)*var.get('b'))+Js(2.0)))
    var.put('b', var.get('getPadThing')(var.get('a').get('a')))
    var.get('a').get('c').callprop('push', var.get('b'))
    var.get('a').put('b', var.get('b').get('length'), '+')
    var.get('b').callprop('push', var.get('a').get('b'))
    return var.get('b')
PyJsHoisted_jb_.func_name = 'jb'
var.put('jb', PyJsHoisted_jb_)
@Js
def PyJsHoisted_encodeCharmListIntoFirstVar_(encodedCharmListHolder, b, c, d, this, arguments, var=var):
    var = Scope({'encodedCharmListHolder':encodedCharmListHolder, 'b':b, 'c':c, 'd':d, 'this':this, 'arguments':arguments}, var)
    var.registers(['c', 'e', 'b', 'encodedCharmListHolder', 'd', 'f'])
    if (var.get(u"null")!=var.get('c')):
        #for JS loop
        var.put('e', Js(0.0))
        while (var.get('e')<var.get('c').get('length')):
            try:
                var.put('f', var.get('jb')(var.get('encodedCharmListHolder'), var.get('b')))
                var.get('d')(var.get('c').get(var.get('e')), var.get('encodedCharmListHolder'))
                var.get('kb')(var.get('encodedCharmListHolder'), var.get('f'))
            finally:
                    (var.put('e',Js(var.get('e').to_number())+Js(1))-Js(1))
PyJsHoisted_encodeCharmListIntoFirstVar_.func_name = 'encodeCharmListIntoFirstVar'
var.put('encodeCharmListIntoFirstVar', PyJsHoisted_encodeCharmListIntoFirstVar_)
@Js
def PyJsHoisted_ib_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    if (Js(0.0)<=var.get('b')):
        var.get('generateNoisyFirstChar')(var.get('a'), var.get('b'))
    else:
        #for JS loop
        var.put('c', Js(0.0))
        while (Js(9.0)>var.get('c')):
            try:
                PyJsComma(var.get('a').get('a').callprop('push', ((var.get('b')&Js(127.0))|Js(128.0))),var.put('b', Js(7.0), '>>'))
            finally:
                    (var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1))
        var.get('a').get('a').callprop('push', Js(1.0))
PyJsHoisted_ib_.func_name = 'ib'
var.put('ib', PyJsHoisted_ib_)
@Js
def PyJsHoisted_lb_(a, b, c, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    ((var.get(u"null")!=var.get('c')) and PyJsComma(var.get('generateNoisyFirstChar')(var.get('a').get('a'), (Js(8.0)*var.get('b'))),var.get('ib')(var.get('a').get('a'), var.get('c'))))
PyJsHoisted_lb_.func_name = 'lb'
var.put('lb', PyJsHoisted_lb_)
@Js
def PyJsHoisted_compressUintMaybe_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', '_item', 'e', 'b', 'item', 'd', 'h', 'index', '_index', 'f'])
    #for JS loop
    var.put('b', var.get('Uint8Array').create((var.get('a').get('b')+var.get('a').get('a').callprop('length'))))
    var.put('c', var.get('a').get('c'))
    var.put('d', var.get('c').get('length'))
    var.put('e', Js(0.0))
    var.put('f', Js(0.0))
    while (var.get('f')<var.get('d')):
        try:
            var.put('h', var.get('c').get(var.get('f')))
            for PyJsTemp in var.get('h'):
                var.put('index', PyJsTemp)
                var.put('item', var.get('h').get(var.get('index')))
                var.get('b').put(var.get('e'), var.get('item'))
                var.get('console').callprop('log', ((var.get('e').callprop('toString')+Js(' '))+var.get('item')))
                (var.put('e',Js(var.get('e').to_number())+Js(1))-Js(1))
        finally:
                (var.put('f',Js(var.get('f').to_number())+Js(1))-Js(1))
    var.put('c', var.get('getPadThing')(var.get('a').get('a')))
    for PyJsTemp in var.get('c'):
        var.put('_index', PyJsTemp)
        var.put('_item', var.get('c').get(var.get('_index')))
        var.get('b').put(var.get('e'), var.get('_item'))
        (var.put('e',Js(var.get('e').to_number())+Js(1))-Js(1))
    var.get('a').put('c', Js([var.get('b')]))
    return var.get('b')
PyJsHoisted_compressUintMaybe_.func_name = 'compressUintMaybe'
var.put('compressUintMaybe', PyJsHoisted_compressUintMaybe_)
@Js
def PyJsHoisted_E_(a, b, c, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'e', 'b', 'd', 'h', 'f'])
    if (var.get(u"null")!=var.get('c')):
        var.put('b', var.get('jb')(var.get('a'), var.get('b')))
        #for JS loop
        var.put('d', var.get('a').get('a'))
        var.put('e', Js(0.0))
        while (var.get('e')<var.get('c').get('length')):
            try:
                var.put('f', var.get('c').callprop('charCodeAt', var.get('e')))
                if (Js(128.0)>var.get('f')):
                    var.get('d').get('a').callprop('push', var.get('f'))
                else:
                    if (Js(2048.0)>var.get('f')):
                        PyJsComma(var.get('d').get('a').callprop('push', ((var.get('f')>>Js(6.0))|Js(192.0))),var.get('d').get('a').callprop('push', ((var.get('f')&Js(63.0))|Js(128.0))))
                    else:
                        if (Js(65536.0)>var.get('f')):
                            if (((Js(55296.0)<=var.get('f')) and (Js(56319.0)>=var.get('f'))) and ((var.get('e')+Js(1.0))<var.get('c').get('length'))):
                                var.put('h', var.get('c').callprop('charCodeAt', (var.get('e')+Js(1.0))))
                                def PyJs_LONG_12_(var=var):
                                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('f', ((((Js(1024.0)*(var.get('f')-Js(55296.0)))+var.get('h'))-Js(56320.0))+Js(65536.0))),var.get('d').get('a').callprop('push', ((var.get('f')>>Js(18.0))|Js(240.0)))),var.get('d').get('a').callprop('push', (((var.get('f')>>Js(12.0))&Js(63.0))|Js(128.0)))),var.get('d').get('a').callprop('push', (((var.get('f')>>Js(6.0))&Js(63.0))|Js(128.0)))),var.get('d').get('a').callprop('push', ((var.get('f')&Js(63.0))|Js(128.0)))),(var.put('e',Js(var.get('e').to_number())+Js(1))-Js(1)))
                                (((Js(56320.0)<=var.get('h')) and (Js(57343.0)>=var.get('h'))) and PyJs_LONG_12_())
                            else:
                                PyJsComma(PyJsComma(var.get('d').get('a').callprop('push', ((var.get('f')>>Js(12.0))|Js(224.0))),var.get('d').get('a').callprop('push', (((var.get('f')>>Js(6.0))&Js(63.0))|Js(128.0)))),var.get('d').get('a').callprop('push', ((var.get('f')&Js(63.0))|Js(128.0))))
            finally:
                    (var.put('e',Js(var.get('e').to_number())+Js(1))-Js(1))
        var.get('kb')(var.get('a'), var.get('b'))
PyJsHoisted_E_.func_name = 'E'
var.put('E', PyJsHoisted_E_)
@Js
def PyJsHoisted_Ob_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    var.put('c', var.get('H')(var.get('a'), Js(1.0), Js('')))
    ((Js(0.0)<var.get('c').get('length')) and var.get('E')(var.get('b'), Js(1.0), var.get('c')))
    var.put('c', var.get('H')(var.get('a'), Js(2.0), Js(0.0)))
    ((PyJsStrictNeq(Js(0.0),var.get('c')) and (var.get(u"null")!=var.get('c'))) and var.get('lb')(var.get('b'), Js(2.0), var.get('c')))
PyJsHoisted_Ob_.func_name = 'Ob'
var.put('Ob', PyJsHoisted_Ob_)
@Js
def PyJsHoisted_K_(a, b, c, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b', 'd'])
    (var.get('a').get('a') or var.get('a').put('a', Js({})))
    if var.get('a').get('a').get(var.get('c')).neg():
        var.put('d', var.get('G')(var.get('a'), var.get('c')))
        (var.get('d') and var.get('a').get('a').put(var.get('c'), var.get('b').create(var.get('d'))))
    return var.get('a').get('a').get(var.get('c'))
PyJsHoisted_K_.func_name = 'K'
var.put('K', PyJsHoisted_K_)
@Js
def PyJsHoisted_Qb_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    var.put('c', var.get('H')(var.get('a'), Js(1.0), Js(0.0)))
    ((PyJsStrictNeq(Js(0.0),var.get('c')) and (var.get(u"null")!=var.get('c'))) and var.get('lb')(var.get('b'), Js(1.0), var.get('c')))
    var.put('c', var.get('H')(var.get('a'), Js(2.0), Js(0.0)))
    ((PyJsStrictNeq(Js(0.0),var.get('c')) and (var.get(u"null")!=var.get('c'))) and var.get('lb')(var.get('b'), Js(2.0), var.get('c')))
    var.put('c', var.get('H')(var.get('a'), Js(3.0), Js(0.0)))
    ((PyJsStrictNeq(Js(0.0),var.get('c')) and (var.get(u"null")!=var.get('c'))) and var.get('lb')(var.get('b'), Js(3.0), var.get('c')))
PyJsHoisted_Qb_.func_name = 'Qb'
var.put('Qb', PyJsHoisted_Qb_)
@Js
def PyJsHoisted_mb_(a, b, c, d, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'c':c, 'd':d, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b', 'd'])
    ((var.get(u"null")!=var.get('c')) and PyJsComma(PyJsComma(var.put('b', var.get('jb')(var.get('a'), var.get('b'))),var.get('d')(var.get('c'), var.get('a'))),var.get('kb')(var.get('a'), var.get('b'))))
PyJsHoisted_mb_.func_name = 'mb'
var.put('mb', PyJsHoisted_mb_)
@Js
def PyJsHoisted_Tb_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'c', 'b'])
    var.put('c', var.get('L')(var.get('a'), var.get('Bb'), Js(1.0)))
    ((Js(0.0)<var.get('c').get('length')) and var.get('encodeCharmListIntoFirstVar')(var.get('b'), Js(1.0), var.get('c'), var.get('Ob')))
    var.put('c', var.get('H')(var.get('a'), Js(2.0), Js(0.0)))
    ((PyJsStrictNeq(Js(0.0),var.get('c')) and (var.get(u"null")!=var.get('c'))) and var.get('lb')(var.get('b'), Js(2.0), var.get('c')))
    var.put('c', var.get('K')(var.get('a'), var.get('Cb'), Js(3.0)))
    ((var.get(u"null")!=var.get('c')) and var.get('mb')(var.get('b'), Js(3.0), var.get('c'), var.get('Qb')))
PyJsHoisted_Tb_.func_name = 'Tb'
var.put('Tb', PyJsHoisted_Tb_)
@Js
def PyJsHoisted_convertToUint_(charmList, this, arguments, var=var):
    var = Scope({'charmList':charmList, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'charmList'])
    var.put('a', var.get('EncodedCharmHolder').create())
    ((Js(0.0)<var.get('charmList').get('length')) and var.get('encodeCharmListIntoFirstVar')(var.get('a'), Js(1.0), var.get('charmList'), var.get('Tb')))
    return var.get('compressUintMaybe')(var.get('a'))
PyJsHoisted_convertToUint_.func_name = 'convertToUint'
var.put('convertToUint', PyJsHoisted_convertToUint_)
@Js
def PyJsHoisted_weirdifyCharms_(charms, this, arguments, var=var):
    var = Scope({'charms':charms, 'this':this, 'arguments':arguments}, var)
    var.registers(['convSlots', 'final', 'skillLevel', 'charms', 'i', 'convd', 'wonky', 'charm', 'skillName'])
    @Js
    def PyJs_convSlots_13_(slots, this, arguments, var=var):
        var = Scope({'slots':slots, 'this':this, 'arguments':arguments, 'convSlots':PyJs_convSlots_13_}, var)
        var.registers(['slots'])
        @Js
        def PyJs_anonymous_14_(x, this, arguments, var=var):
            var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
            var.registers(['x'])
            return (var.get('x') if var.get('x').neg().neg() else var.get(u"null"))
        PyJs_anonymous_14_._set_name('anonymous')
        return var.get('slots').callprop('map', PyJs_anonymous_14_)
    PyJs_convSlots_13_._set_name('convSlots')
    var.put('convSlots', PyJs_convSlots_13_)
    var.put('final', Js([]))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('charms').get('length')):
        try:
            var.put('charm', var.get('charms').get(var.get('i')))
            var.put('wonky', Js({'j':var.get(u"null"),'c':(-Js(1.0)),'F':Js([Js([]), Js([])]),'f':Js(1.7976931348623157e+308),'i':Js({}),'a':Js({'1':Js([]),'3':Js({'a':var.get(u"null"),'j':var.get(u"null"),'c':(-Js(1.0)),'F':Js([]),'f':Js(1.7976931348623157e+308),'i':Js({})})})}))
            @Js
            def PyJs_anonymous_15_(x, this, arguments, var=var):
                var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
                var.registers(['x'])
                return (var.get('x')==Js(0.0))
            PyJs_anonymous_15_._set_name('anonymous')
            if var.get('charm').get('slots').callprop('every', PyJs_anonymous_15_).neg():
                var.put('convd', var.get('convSlots')(var.get('charm').get('slots')))
                var.get('wonky').get('F').get('1').callprop('push', var.get('convd'))
                var.get('wonky').get('a').get('3').put('F', var.get('convd'))
            for PyJsTemp in var.get('charm').get('skills'):
                var.put('skillName', PyJsTemp)
                var.put('skillLevel', var.get('charm').get('skills').get(var.get('skillName')))
                var.get('wonky').get('F').get('0').callprop('push', Js([var.get('skillName'), var.get('skillLevel')]))
                var.get('wonky').get('a').get('1').callprop('push', Js({'a':var.get(u"null"),'j':var.get(u"null"),'c':(-Js(1.0)),'F':Js([var.get('skillName'), var.get('skillLevel')]),'f':Js(1.7976931348623157e+308),'i':Js({})}))
            var.get('final').callprop('push', var.get('wonky'))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return var.get('final')
PyJsHoisted_weirdifyCharms_.func_name = 'weirdifyCharms'
var.put('weirdifyCharms', PyJsHoisted_weirdifyCharms_)
@Js
def PyJsHoisted_loadCharmsFromFile_(charmFile, this, arguments, var=var):
    var = Scope({'charmFile':charmFile, 'this':this, 'arguments':arguments}, var)
    var.registers(['charms', 'charm_data', 'charmFile'])
    if var.get('charmFile').callprop('endsWith', Js('.json')).neg():
        var.get('console').callprop('error', Js('Invalid charm file, pass one json charm file'))
        PyJsTempException = JsToPyException(var.get('Error')(Js('Invalid charm file, pass one json charm file')))
        raise PyJsTempException
    var.put('charm_data', var.get('require')(Js('fs')).callprop('readFileSync', var.get('charmFile')))
    var.put('charms', Js([]))
    try:
        var.put('charms', var.get('JSON').callprop('parse', var.get('charm_data')))
    except PyJsException as PyJsTempException:
        PyJsHolder_65_81837740 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            var.get('console').callprop('error', Js('Invalid charm file, Could not parse'))
            PyJsTempException = JsToPyException(var.get('e'))
            raise PyJsTempException
        finally:
            if PyJsHolder_65_81837740 is not None:
                var.own['e'] = PyJsHolder_65_81837740
            else:
                del var.own['e']
            del PyJsHolder_65_81837740
    return var.get('charms')
PyJsHoisted_loadCharmsFromFile_.func_name = 'loadCharmsFromFile'
var.put('loadCharmsFromFile', PyJsHoisted_loadCharmsFromFile_)
@Js
def PyJsHoisted_loadCharmFromLoadedJsonString_(charm_data, this, arguments, var=var):
    var = Scope({'charm_data':charm_data, 'this':this, 'arguments':arguments}, var)
    var.registers(['charms', 'charm_data'])
    var.put('charms', Js([]))
    try:
        var.put('charms', var.get('JSON').callprop('parse', var.get('charm_data')))
    except PyJsException as PyJsTempException:
        PyJsHolder_65_62778639 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            var.get('console').callprop('error', Js('Invalid charm data, Could not parse'))
        finally:
            if PyJsHolder_65_62778639 is not None:
                var.own['e'] = PyJsHolder_65_62778639
            else:
                del var.own['e']
            del PyJsHolder_65_62778639
    return var.get('charms')
PyJsHoisted_loadCharmFromLoadedJsonString_.func_name = 'loadCharmFromLoadedJsonString'
var.put('loadCharmFromLoadedJsonString', PyJsHoisted_loadCharmFromLoadedJsonString_)
@Js
def PyJsHoisted_encodeCharms_(charmsFromJson, this, arguments, var=var):
    var = Scope({'charmsFromJson':charmsFromJson, 'this':this, 'arguments':arguments}, var)
    var.registers(['charmsFromJson', 'converted', 'charmList'])
    var.put('charmList', var.get('weirdifyCharms')(var.get('charmsFromJson')))
    var.put('converted', var.get('convertToUint')(var.get('charmList')))
    var.get('console').callprop('log', var.get('converted'))
    var.get('console').callprop('log', (Js('undefined') if PyJsStrictEq(var.get('converted',throw=False).typeof(),Js('undefined')) else var.get('_typeof')(var.get('converted'))))
    var.put('encoded', var.get('btoa_func')(var.get('String').get('fromCharCode').callprop('apply', var.get(u"null"), var.get('converted'))))
    return var.get('encoded')
PyJsHoisted_encodeCharms_.func_name = 'encodeCharms'
var.put('encodeCharms', PyJsHoisted_encodeCharms_)
@Js
def PyJsHoisted_saveEncodedCharms_(encodedCharms, this, arguments, var=var):
    var = Scope({'encodedCharms':encodedCharms, 'this':this, 'arguments':arguments}, var)
    var.registers(['encodedCharms', 'encodedCharmsFile'])
    var.put('encodedCharmsFile', (var.get('arguments').get('1') if ((var.get('arguments').get('length')>Js(1.0)) and PyJsStrictNeq(var.get('arguments').get('1'),var.get('undefined'))) else Js('charms.encoded.txt')))
    var.get('require')(Js('fs')).callprop('writeFileSync', var.get('encodedCharmsFile'), var.get('encodedCharms'))
PyJsHoisted_saveEncodedCharms_.func_name = 'saveEncodedCharms'
var.put('saveEncodedCharms', PyJsHoisted_saveEncodedCharms_)
@Js
def PyJsHoisted_encodeFromPython_(charmData, this, arguments, var=var):
    var = Scope({'charmData':charmData, 'this':this, 'arguments':arguments}, var)
    var.registers(['charms', 'encodedCharms', 'charmData'])
    var.put('charms', var.get('loadCharmFromLoadedJsonString')(var.get('charmData')))
    var.put('encodedCharms', var.get('encodeCharms')(var.get('charms')))
    var.get('console').callprop('log', var.get('encodedCharms'))
PyJsHoisted_encodeFromPython_.func_name = 'encodeFromPython'
var.put('encodeFromPython', PyJsHoisted_encodeFromPython_)
@Js
def PyJsHoisted_main_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['charms', 'encodedCharms', 'charm_file', 'args'])
    var.put('args', var.get('process').get('argv'))
    var.get('console').callprop('log', var.get('args'))
    var.put('charm_file', var.get('args').callprop('pop'))
    var.put('charms', var.get('loadCharmsFromFile')(var.get('charm_file')))
    var.put('encodedCharms', var.get('encodeCharms')(var.get('charms')))
    var.get('console').callprop('log', var.get('encodedCharms'))
    var.get('saveEncodedCharms')(var.get('encodedCharms'))
PyJsHoisted_main_.func_name = 'main'
var.put('main', PyJsHoisted_main_)
Js('use strict')
@Js
def PyJs_anonymous_0_(obj, this, arguments, var=var):
    var = Scope({'obj':obj, 'this':this, 'arguments':arguments}, var)
    var.registers(['obj'])
    return var.get('obj',throw=False).typeof()
PyJs_anonymous_0_._set_name('anonymous')
@Js
def PyJs_anonymous_1_(obj, this, arguments, var=var):
    var = Scope({'obj':obj, 'this':this, 'arguments':arguments}, var)
    var.registers(['obj'])
    return (Js('symbol') if (((var.get('obj') and PyJsStrictEq(var.get('Symbol',throw=False).typeof(),Js('function'))) and PyJsStrictEq(var.get('obj').get('constructor'),var.get('Symbol'))) and PyJsStrictNeq(var.get('obj'),var.get('Symbol').get('prototype'))) else var.get('obj',throw=False).typeof())
PyJs_anonymous_1_._set_name('anonymous')
var.put('_typeof', (PyJs_anonymous_0_ if (PyJsStrictEq(var.get('Symbol',throw=False).typeof(),Js('function')) and PyJsStrictEq(var.get('Symbol').get('iterator').typeof(),Js('symbol'))) else PyJs_anonymous_1_))
@Js
def PyJs_anonymous_2_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['defineProperties'])
    @Js
    def PyJsHoisted_defineProperties_(target, props, this, arguments, var=var):
        var = Scope({'target':target, 'props':props, 'this':this, 'arguments':arguments}, var)
        var.registers(['i', 'props', 'descriptor', 'target'])
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('props').get('length')):
            try:
                var.put('descriptor', var.get('props').get(var.get('i')))
                var.get('descriptor').put('enumerable', (var.get('descriptor').get('enumerable') or Js(False)))
                var.get('descriptor').put('configurable', Js(True))
                if var.get('descriptor').contains(Js('value')):
                    var.get('descriptor').put('writable', Js(True))
                var.get('Object').callprop('defineProperty', var.get('target'), var.get('descriptor').get('key'), var.get('descriptor'))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    PyJsHoisted_defineProperties_.func_name = 'defineProperties'
    var.put('defineProperties', PyJsHoisted_defineProperties_)
    pass
    @Js
    def PyJs_anonymous_3_(Constructor, protoProps, staticProps, this, arguments, var=var):
        var = Scope({'Constructor':Constructor, 'protoProps':protoProps, 'staticProps':staticProps, 'this':this, 'arguments':arguments}, var)
        var.registers(['protoProps', 'Constructor', 'staticProps'])
        if var.get('protoProps'):
            var.get('defineProperties')(var.get('Constructor').get('prototype'), var.get('protoProps'))
        if var.get('staticProps'):
            var.get('defineProperties')(var.get('Constructor'), var.get('staticProps'))
        return var.get('Constructor')
    PyJs_anonymous_3_._set_name('anonymous')
    return PyJs_anonymous_3_
PyJs_anonymous_2_._set_name('anonymous')
var.put('_createClass', PyJs_anonymous_2_())
pass
var.put('qb', Js([]))
var.put('ob', (Js('function')==var.get('Uint8Array',throw=False).typeof()))
@Js
def PyJs_btoa_func_4_(str, this, arguments, var=var):
    var = Scope({'str':str, 'this':this, 'arguments':arguments, 'btoa_func':PyJs_btoa_func_4_}, var)
    var.registers(['str'])
    if PyJsStrictEq(var.get('module',throw=False).typeof(),Js('undefined')):
        return var.get('btoa')(var.get('str'))
    else:
        return var.get('Buffer').callprop('from', var.get('str'), Js('latin1')).callprop('toString', Js('base64'))
PyJs_btoa_func_4_._set_name('btoa_func')
var.put('btoa_func', PyJs_btoa_func_4_)
@Js
def PyJs_anonymous_5_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['BufferTypeThing'])
    @Js
    def PyJsHoisted_BufferTypeThing_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        var.get('_classCallCheck')(var.get(u"this"), var.get('BufferTypeThing'))
        var.get(u"this").put('a', Js([]))
    PyJsHoisted_BufferTypeThing_.func_name = 'BufferTypeThing'
    var.put('BufferTypeThing', PyJsHoisted_BufferTypeThing_)
    pass
    @Js
    def PyJs_length_6_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'length':PyJs_length_6_}, var)
        var.registers([])
        return var.get(u"this").get('a').get('length')
    PyJs_length_6_._set_name('length')
    var.get('_createClass')(var.get('BufferTypeThing'), Js([Js({'key':Js('length'),'value':PyJs_length_6_})]))
    return var.get('BufferTypeThing')
PyJs_anonymous_5_._set_name('anonymous')
var.put('BufferTypeThing', PyJs_anonymous_5_())
@Js
def PyJs_EncodedCharmHolder_7_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments, 'EncodedCharmHolder':PyJs_EncodedCharmHolder_7_}, var)
    var.registers([])
    var.get('_classCallCheck')(var.get(u"this"), var.get('EncodedCharmHolder'))
    var.get(u"this").put('c', Js([]))
    var.get(u"this").put('b', Js(0.0))
    var.get(u"this").put('a', var.get('BufferTypeThing').create())
PyJs_EncodedCharmHolder_7_._set_name('EncodedCharmHolder')
var.put('EncodedCharmHolder', PyJs_EncodedCharmHolder_7_)
@Js
def PyJs_anonymous_8_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['Bb'])
    @Js
    def PyJsHoisted_Bb_(a, this, arguments, var=var):
        var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
        var.registers(['a'])
        var.get('_classCallCheck')(var.get(u"this"), var.get('Bb'))
        var.get('pb')(var.get(u"this"), var.get('a'), var.get(u"null"), var.get(u"null"))
    PyJsHoisted_Bb_.func_name = 'Bb'
    var.put('Bb', PyJsHoisted_Bb_)
    pass
    @Js
    def PyJs_K_9_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'K':PyJs_K_9_}, var)
        var.registers(['a'])
        var.put('a', var.get('EncodedCharmHolder').create())
        var.get('Ob')(var.get(u"this"), var.get('a'))
        return var.get('compressUintMaybe')(var.get('a'))
    PyJs_K_9_._set_name('K')
    var.get('_createClass')(var.get('Bb'), Js([Js({'key':Js('K'),'value':PyJs_K_9_})]))
    return var.get('Bb')
PyJs_anonymous_8_._set_name('anonymous')
var.put('Bb', PyJs_anonymous_8_())
@Js
def PyJs_anonymous_10_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['Cb'])
    @Js
    def PyJsHoisted_Cb_(a, this, arguments, var=var):
        var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
        var.registers(['a'])
        var.get('_classCallCheck')(var.get(u"this"), var.get('Cb'))
        var.get('pb')(var.get(u"this"), var.get('a'), var.get(u"null"), var.get(u"null"))
    PyJsHoisted_Cb_.func_name = 'Cb'
    var.put('Cb', PyJsHoisted_Cb_)
    pass
    @Js
    def PyJs_K_11_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments, 'K':PyJs_K_11_}, var)
        var.registers(['a'])
        var.put('a', var.get('EncodedCharmHolder').create())
        var.get('Qb')(var.get(u"this"), var.get('a'))
        return var.get('compressUintMaybe')(var.get('a'))
    PyJs_K_11_._set_name('K')
    var.get('_createClass')(var.get('Cb'), Js([Js({'key':Js('K'),'value':PyJs_K_11_})]))
    return var.get('Cb')
PyJs_anonymous_10_._set_name('anonymous')
var.put('Cb', PyJs_anonymous_10_())
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
if PyJsStrictNeq(var.get('module',throw=False).typeof(),Js('undefined')):
    var.get('main')()
pass


# Add lib to the module scope
py_encoder = var.to_python()