
window.addEvent('domready',function(){if(Browser.ie&&Browser.version<=7){var key='ie7_update_tip';if(Cookie.read(key)){return;}
var html='\
      <div class="pageCover" style="position:fixed;height:100%;display:block"></div>\
      <div class="container textCenter">\
        <p class="f14px cTitle">Ϊ�˻�ø��õ�������飬������ʹ������������򿪲ر���</p>\
        <div class="cBList">\
          <a class="cItem" href="http://www.google.cn/chrome/browser/desktop/index.html" target="_blank"><i class="bw bw4"></i>����chrome</a>\
          <a class="cItem" href="https://support.microsoft.com/zh-cn/help/17621/internet-explorer-downloads" target="_blank"><i class="bw bw1"></i>����IE10.0</a>\
          <a class="cItem" href="http://www.firefox.com.cn/download/" target="_blank"><i class="bw bw2"></i>���ػ��</a>\
          <a class="cItem" href="http://se.360.cn/" target="_blank"><i class="bw bw3"></i>����360</a>\
        </div>\
        <a href="javascript:;" class="btn1 cContinue">�������</a>\
      </div>\
    ';var $body=$(document.body||document.getElementsByTagName('body')[0]);var $root=new Element('div',{id:'ie7_update_tip',html:html});$body.grabBottom($root);$root.addEvent('click:relay(.cContinue)',function(){$root.setStyle('display','none');Cookie.write(key,1,{domain:document.domain.split('.').slice(1).join('.')});});}});