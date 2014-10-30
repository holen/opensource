server {
    listen       80;
    server_name  test.com;

    if ( $http_user_agent ~ "^((.*MIDP.*)|(.*WAP.*)|(.*UP.Browser.*)|(.*Smartphone.*)|(.*Obigo.*)|(.*Mobile.*)|(.*AU.Browser.*)|(.*wxd.Mms.*)|(.*WxdB.Browser.*)|(.*CLDC.*)|(.*UP.Link.*)|(.*KM.Browser.*)|(.*UCWEB.*)|(.*SEMC\-Browser.*)|(.*Mini.*)|(.*Symbian.*)|(.*Palm.*)|(.*Nokia.*)|(.*Panasonic.*)|(.*MOT\-.*)|(.*SonyEricsson.*)|(.*NEC\-.*)|(.*Alcatel.*)|(.*Ericsson.*)|(.*BENQ.*)|(.*BenQ.*)|(.*Amoisonic.*)|(.*Amoi\-.*)|(.*Capitel.*)|(.*PHILIPS.*)|(.*SAMSUNG.*)|(.*Lenovo.*)|(.*Mitsu.*)|(.*Motorola.*)|(.*SHARP.*)|(.*WAPPER.*)|(.*LG\-.*)|(.*LG/.*)|(.*EG900.*)|(.*CECT.*)|(.*Compal.*)|(.*kejian.*)|(.*Bird.*)|(.*BIRD.*)|(.*G900/V1.0.*)|(.*Arima.*)|(.*CTL.*)|(.*TDG.*)|(.*Daxian.*)|(.*DAXIAN.*)|(.*DBTEL.*)|(.*Eastcom.*)|(.*EASTCOM.*)|(.*PANTECH.*)|(.*Dopod.*)|(.*Haier.*)|(.*HAIER.*)|(.*KONKA.*)|(.*KEJIAN.*)|(.*LENOVO.*)|(.*Soutec.*)|(.*SOUTEC.*)|(.*SAGEM.*)|(.*SEC\-.*)|(.*SED\-.*)|(.*EMOL\-.*)|(.*INNO55.*)|(.*ZTE.*)|(.*iPhone.*)|(.*Android.*)|(.*Windows CE.*)|(java.*)|(Opera.*))$" ){
        rewrite "^.*$" /2.html break;
    }

    location / {
        root    html;
        index   1.html;
    }
}

