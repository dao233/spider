function test() {
    function h(a, c) {
        return Math.floor(Math.random() * (c - a) + a)
    }
    function k() {
        var a = Math.random().toString(36).substr(2, 6);
        return b[a] ? k() : a
    }
    function f(a, c) {
        var d = new Image,
        b = getDomain();
        d.src = location.protocol + "//pb.sogou.com/pv.gif?uigs_productid=webapp&type=antispider&subtype=" + a + "&domain=" + b + "&suv=" + getCookie("SUV") + "&snuid=" + getCookie("SNUID") + "&t=" + (new Date).getTime() + (c ? "&" + c: "")
        //pb.sogou.com/pv.gif?uigs_productid=webapp&type=antispider&subtype=verify_page&domain=
    }

    var n = '/web?query=inurl:fc234c36eef8463483462569fb333e88+site:sxkid.com&_asf=www.sogou.com&_ast=&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index&sut=2465&sst0=1589792831835&lkt=53,1589792831835,1589792832292&sugsuv=1589792831779908&sugtime=1589792831835',
    l = new Date(1589792833000),
    e = parseInt(getCookie("ABTEST")[0]),
    g = getCookie("SUID"),
    p = navigator.userAgent,
    m = h(e, g.length),
    b = {
        sn: g.substring(e, m + 1)
    }; (function(a) {
        if ( - 2 < p.indexOf("MSIE")) {
            var c = l.getHours(),
            d = b.sn;
            d += a[c];
            b.sn = d
        }
    })(g);
    console.log(b);
    for (e = 1; e < m; e++) b[k()] = h(0, l.getSeconds());
    $.ajax({
        url: "http://www.sogou.com/antispider/detect.php",
        type: "GET",
        cache: !1,
        data: b,
        dataType: "json",
        success: function(a) {
            if (0 !== a.code) {
                var c = (~location.search.indexOf("?") ? "&": "?") + "verify=0";
                setTimeout(function() {
                    location.href += c
                },
                50);
                f("verify_page", "faile")
            } else {
                f("verify_page", "success");
                var d = new Date,
                b = "sogou.com";
                "snapshot.sogoucdn.com" == location.hostname && (b = "snapshot.sogoucdn.com");
                getCookie("SNUID") || (d.setTime(d.getTime() + 31536E6), setCookie("SNUID", a.id, d.toGMTString(), b, "/"));
                setTimeout(function() {
                    location.href = encodeURI(n)
                },
                50)
            }
        }
    });
    f("verify_page", "pv")
};