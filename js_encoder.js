
var qb = [];
var ob = "function" == typeof Uint8Array;
const btoa_func = (str) => {
    if (typeof module === 'undefined')
        // return btoa(str);
        return str.toString('base64');
    else {
        return Buffer.from(str, 'latin1').toString('base64');
    }
};

class BufferTypeThing {
    constructor() {
        this.a = [];
    }
    length() {
        return this.a.length;
    }
}

class EncodedCharmHolder {
    constructor() {
        this.c = [];
        this.b = 0;
        this.a = new BufferTypeThing();
    }
}
class Bb {
    constructor(a) {
        pb(this, a, null, null);
    }
    K() {
        var a = new EncodedCharmHolder();
        Ob(this, a);
        return compressUintMaybe(a);
    }
}
class Cb {
    constructor(a) {
        pb(this, a, null, null);
    }
    K() {
        var a = new EncodedCharmHolder();
        Qb(this, a);
        return compressUintMaybe(a);
    }
}

function L(a, b, c) {
    wb(a, b, c);
    b = a.a[c];
    b == qb && (b = a.a[c] = []);
    return b;
}

function wb(a, b, c) {
    a.a || (a.a = {});
    if (!a.a[c]) {
        var d = G(a, c)
        var e = [];
        for (var f = 0; f < d.length; f++) e[f] = new b(d[f]);
        a.a[c] = e;
    }
}

function G(a, b) {
    if (b < a.f) {
        b += a.c;
        var c = a.F[b];
        return c === qb ? (a.F[b] = []) : c;
    }
    if (a.b) return (c = a.b[b]), c === qb ? (a.b[b] = []) : c;
}
function H(a, b, c) {
    a = G(a, b);
    return null == a ? c : a;
}

function fa(a) {
    var b = typeof a;
    if ("object" == b)
        if (a) {
            if (a instanceof Array) return "array";
            if (a instanceof Object) return b;
            var c = Object.prototype.toString.call(a);
            if ("[object Window]" == c) return "object";
            if ("[object Array]" == c || ("number" == typeof a.length && "undefined" != typeof a.splice && "undefined" != typeof a.propertyIsEnumerable && !a.propertyIsEnumerable("splice"))) return "array";
            if ("[object Function]" == c || ("undefined" != typeof a.call && "undefined" != typeof a.propertyIsEnumerable && !a.propertyIsEnumerable("call"))) return "function";
        } else return "null";
    else if ("function" == b && "undefined" == typeof a.call) return "object";
    return b;
}

function rb(a) {
    var b = a.f + a.c;
    a.F[b] || (a.b = a.F[b] = {});
}

function tb(a, b, c) {
    b < a.f ? (a.F[b + a.c] = c) : (rb(a), (a.b[b] = c));
}

function sb(a, b) {
    for (var c, d, e = 0; e < b.length; e++) {
        var f = b[e],
            h = G(a, f);
        null != h && ((c = f), (d = h), tb(a, f, void 0));
    }
    return c ? (tb(a, c, d), c) : 0;
}

function pb(a, b, c, d) {
    a.a = null;
    b || (b = []);
    a.j = void 0;
    a.c = -1;
    a.F = b;
    a: {
        if ((b = a.F.length)) {
            --b;
            var e = a.F[b];
            if (!(null === e || "object" != typeof e || "array" == fa(e) || (ob && e instanceof Uint8Array))) {
                a.f = b - a.c;
                a.b = e;
                break a;
            }
        }
        a.f = Number.MAX_VALUE;
    }
    // if ((b = a.F.length)) {
    //     --b;
    //     var e = a.F[b];
    //     if (!(null === e || "object" != typeof e || "array" == fa(e) || (ob && e instanceof Uint8Array))) {
    //         a.f = b - a.c;
    //         a.b = e;
    //     } else {
    //         a.f = Number.MAX_VALUE;

    //     }
    // } else {
    //     a.f = Number.MAX_VALUE;
    // }
    a.i = {};
    if (c) for (b = 0; b < c.length; b++) (e = c[b]), e < a.f ? ((e += a.c), (a.F[e] = a.F[e] || qb)) : (rb(a), (a.b[e] = a.b[e] || qb));
    if (d && d.length) for (b = 0; b < d.length; b++) sb(a, d[b]);
}
function getPadThing(a) {
    var b = a.a;
    a.a = [];
    return b;
}
function generateNoisyFirstChar(a, b) {
    for (; 127 < b;) a.a.push((b & 127) | 128), (b >>>= 7);
    a.a.push(b);
}
function kb(a, b) {
    var c = b.pop();
    c = a.b + a.a.length() - c
    for (; 127 < c;) {
        b.push((c & 127) | 128);
        (c >>>= 7);
        a.b++;
    }
    b.push(c);
    a.b++;
}
function jb(a, b) {
    generateNoisyFirstChar(a.a, 8 * b + 2);
    b = getPadThing(a.a);
    a.c.push(b);
    a.b += b.length;
    b.push(a.b);
    return b;
}

function encodeCharmListIntoFirstVar(encodedCharmListHolder, b, c, d) {
    if (null != c)
        for (var e = 0; e < c.length; e++) {
            var f = jb(encodedCharmListHolder, b);
            d(c[e], encodedCharmListHolder);
            kb(encodedCharmListHolder, f);
        }
}

function ib(a, b) {
    if (0 <= b) generateNoisyFirstChar(a, b);
    else {
        for (var c = 0; 9 > c; c++) {
            a.a.push((b & 127) | 128);
            (b >>= 7);
        }
        a.a.push(1);
    }
}

function lb(a, b, c) {
    null != c && (generateNoisyFirstChar(a.a, 8 * b), ib(a.a, c));
}

function compressUintMaybe(a) {
    for (var b = new Uint8Array(a.b + a.a.length()), c = a.c, d = c.length, e = 0, f = 0; f < d; f++) {
        var h = c[f];
        for (let index in h) {
            let item = h[index] //needed for js2py
            b[e] = item;
            e++;
        }
    }
    c = getPadThing(a.a);

    for (let index in c) {
        let item = c[index] //needed for js2py
        b[e] = item;
        e++;
    }
    a.c = [b];
    return b;
}

function E(a, b, c) {
    if (null != c) {
        b = jb(a, b);
        for (var d = a.a, e = 0; e < c.length; e++) {
            var f = c.charCodeAt(e);
            if (128 > f) d.a.push(f);
            else if (2048 > f) d.a.push((f >> 6) | 192), d.a.push((f & 63) | 128);
            else if (65536 > f)
                if (55296 <= f && 56319 >= f && e + 1 < c.length) {
                    var h = c.charCodeAt(e + 1);
                    56320 <= h && 57343 >= h && ((f = 1024 * (f - 55296) + h - 56320 + 65536), d.a.push((f >> 18) | 240), d.a.push(((f >> 12) & 63) | 128), d.a.push(((f >> 6) & 63) | 128), d.a.push((f & 63) | 128), e++);
                } else d.a.push((f >> 12) | 224), d.a.push(((f >> 6) & 63) | 128), d.a.push((f & 63) | 128);
        }
        kb(a, b);
    }
}
function Ob(a, b) {
    var c = H(a, 1, "");
    0 < c.length && E(b, 1, c);
    c = H(a, 2, 0);
    0 !== c && null != c && lb(b, 2, c);
}

function K(a, b, c) {
    a.a || (a.a = {});
    if (!a.a[c]) {
        var d = G(a, c);
        d && (a.a[c] = new b(d));
    }
    return a.a[c];
}


function Qb(a, b) {
    var c = H(a, 1, 0);
    0 !== c && null != c && lb(b, 1, c);
    c = H(a, 2, 0);
    0 !== c && null != c && lb(b, 2, c);
    c = H(a, 3, 0);
    0 !== c && null != c && lb(b, 3, c);
}

function mb(a, b, c, d) {
    null != c && ((b = jb(a, b)), d(c, a), kb(a, b));
}

function Tb(a, b) {
    var c = L(a, Bb, 1);
    0 < c.length && encodeCharmListIntoFirstVar(b, 1, c, Ob);
    c = H(a, 2, 0);
    0 !== c && null != c && lb(b, 2, c);
    c = K(a, Cb, 3);
    null != c && mb(b, 3, c, Qb);
}


function convertToUint(charmList) {
    var a = new EncodedCharmHolder()
    0 < charmList.length && encodeCharmListIntoFirstVar(a, 1, charmList, Tb);
    return compressUintMaybe(a);
};


function weirdifyCharms(charms) {
    let convSlots = (slots) => slots.map(x => !!x ? x : null)
    const final = []

    for (let i = 0; i < charms.length; i++) {
        let charm = charms[i];
        let wonky = {
            j: null,
            c: -1,
            F: [
                [
                ],
                [
                ],
            ],
            f: Number.MAX_VALUE,
            i: {},
            a: {
                "1": [
                ],
                "3": {
                    a: null,
                    j: null,
                    c: -1,
                    F: [
                    ],
                    f: Number.MAX_VALUE,
                    i: {
                    },
                },
            }
        }
        if (!charm['slots'].every(x => x == 0)) {
            const convd = convSlots(charm['slots']);
            wonky.F[1].push(convd);
            wonky.a["3"].F = convd;
        }
        for (let skillName in charm['skills']) {
            let skillLevel = charm['skills'][skillName]
            wonky.F[0].push([skillName, skillLevel])
            wonky.a["1"].push({
                a: null,
                j: null,
                c: -1,
                F: [
                    skillName,
                    skillLevel,
                ],
                f: Number.MAX_VALUE,
                i: {
                },
            })
        }
        final.push(wonky);
    }
    return final
}

function loadCharmsFromFile(charmFile) {
    if (!charmFile.endsWith(".json")) {
        console.error("Invalid charm file, pass one json charm file");
        throw Error("Invalid charm file, pass one json charm file")
    }

    let charm_data = require("fs").readFileSync(charmFile);

    let charms = [];
    try {
        charms = JSON.parse(charm_data);
    } catch (e) {
        console.error("Invalid charm file, Could not parse");
        throw (e)
    }
    return charms;
}

function loadCharmFromLoadedJsonString(charm_data) {
    let charms = [];
    try {
        charms = JSON.parse(charm_data);
    } catch (e) {
        console.error("Invalid charm data, Could not parse");
    }
    return charms;
}

function encodeCharms(charmsFromJson) {
    let charmList = weirdifyCharms(charmsFromJson)
    let converted = convertToUint(charmList)
    // console.log(converted)
    let encoded = btoa_func(String.fromCharCode.apply(null, converted))
    return encoded
}

function saveEncodedCharms(encodedCharms, encodedCharmsFile = "charms.encoded.txt") {
    require("fs").writeFileSync(encodedCharmsFile, encodedCharms)
}

function encodeFromPython(charmData) {
    let charms = loadCharmFromLoadedJsonString(charmData);
    let encodedCharms = encodeCharms(charms);
    console.log(encodedCharms);
    return encodedCharms;
}

function main() {
    let args = process.argv
    // console.log(args)
    let charm_file = args.pop()

    let charms = loadCharmsFromFile(charm_file)
    let encodedCharms = encodeCharms(charms)
    // console.log(encodedCharms)
    saveEncodedCharms(encodedCharms)
}

if (typeof module !== 'undefined') {
    main();
}
