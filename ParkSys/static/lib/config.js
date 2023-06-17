var defaultOpt = {
  mapDataUrl: "../data",
  mapThemeUrl: "../data/theme",
  mapID: "test666",
  themeID: 1004,
  mapEffectUrl: "../data/effects",
  effectThemeID: "E001",
  origin: window.origin + '/escopemap/content/cn/indoor-sdk'
};
function getQueryString(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
  var r = window.location.search.substr(1).match(reg);
  if (r != null) return unescape(r[2]);
  return null;
}

function tipClick(route,name){
  var origin = defaultOpt.origin
  origin += route
  if(name){
    window.sdkApiName = name
  }
  window.open(origin)
}

(
  //tips
  function() {
    window.MaskLayer = {
      _layer: null,
      show: function(element) {
        return;
        if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) return; //手机不显示
        var _this = this;
        element = element || document.body;
        if (MaskLayer._layer && MaskLayer._layer.parentNode) {
          MaskLayer._layer.parentNode.removeChild(MaskLayer._layer);
        }
        MaskLayer._layer = document.createElement("div");
        MaskLayer._layer.className = "mask-layer-container";
        element.appendChild(MaskLayer._layer);
        var outer = document.createElement("div");
        outer.className = "tip-outer";
        var inner = document.createElement("div");
        inner.className = "tip-inner";

        var content =
          "<h2 class='t-1'> <small>左键</small>平移</h2> <h2 class='t-2'> <small>右键</small>旋转</h2><h2 class='t-3'> <small>滚轮</small>缩放</h2> <div class='t-close'>知道了</div>";
        inner.innerHTML = content;

        outer.appendChild(inner);
        MaskLayer._layer.appendChild(outer);
        outer.style.cssText =
          " position: absolute; z-index: 999;width:100%;height: 100%; background: rgba(0,0,0,0.6);display: flex;justify-content: center;align-items:center;color:#fff;";
        inner.style.position = "relative";
        inner.style.background = "url('../image/tips.png') no-repeat";
        inner.style.width = "300px";
        inner.style.height = "300px";

        document.querySelector(".tip-outer h2:nth-of-type(1)").style.cssText =
          "position:absolute;bottom:97px;left:-106px;letterSpacint:3px;";
        document.querySelector(".tip-outer h2:nth-of-type(2)").style.cssText =
          "position:absolute;right:-103px;top:32px;letterSpacint:3px;";
        document.querySelector(".tip-outer h2:nth-of-type(3)").style.cssText =
          "position:absolute;bottom:83px;right:-104px;letterSpacint:3px;";
        var tclose = document.querySelector(".tip-inner  .t-close");
        tclose.style.cssText =
          "position:absolute;bottom:-97px;left:50%;margin-left:-37px;padding:10px 28px;border:2px solid #fff;border-radius:8px;cursor:pointer;font-size:20px;font-weight:600";

        var layer = document.querySelector(".mask-layer-container");
        layer.style.cssText =
          "position: fixed; left: 0; right: 0; top: 0; bottom: 0; background-color: rgba(0,0,0,0.6); opacity: 0;transition:opacity 0.5s; -webkit-transition: opacity 0.5s; z-index: 800;";

        tclose.onclick = function() {
          _this.hide();
        };
        window.setTimeout(function() {
          MaskLayer._layer.className = MaskLayer._layer.className + " show";
          var layershow = document.querySelector(".mask-layer-container.show");
          layershow.style.opacity = 1;
        }, 10);
      },
      hide: function() {
        if (!MaskLayer._layer) return;
        MaskLayer._layer.className = MaskLayer._layer.className.replace(
          /show/g,
          ""
        );
        window.setTimeout(function() {
          if (!MaskLayer._layer) return;
          MaskLayer._layer.parentNode.removeChild(MaskLayer._layer);
          MaskLayer._layer = null;
        }, 200);
      }
    };
    var tiped = window.localStorage.getItem("esmap_tiped");
    if (!tiped) {
      setTimeout(function() {
        window.MaskLayer.show();
        localStorage.setItem("esmap_tiped", true);
      }, 3000);
    }
  }
)();
(function() {
  function ckCode(url, ismain) {
    if (ismain) {
      var content = $("#container").contents();
      content.find(".tips-right .showCode").remove();
      content
        .find(".tips-right")
        .prepend(
          '<a href="' +
            url +
            '" target="_blank" class="showCode" title="\u4E0B\u8F7D\u793A\u4F8B" style="display: inline-block;width: 34px;height: 100%;background: url(../image/download.png) no-repeat center;background-size: 60%;"></a>'
        );
    } else {
      var content = $(document.body);
      content.find(".tips-right .showCode").remove();
      content
        .find(".tips-right")
        .prepend(
          '<a href="' +
            url +
            '" target="_blank" class="showCode" title="\u4E0B\u8F7D\u793A\u4F8B" style="display: inline-block;width: 34px;height: 100%;background: url(../image/download.png) no-repeat center;background-size: 60%;"></a>'
        );
    }
  }
  window.onload = function() {
    var ct = $(".tips-right");
    ct.find(".showCode").remove();
    ct.prepend('<a href="https://www.esmap.cn/docs/down/" target="_blank" class="showCode" title="下载" style="display: inline-block;width: 34px;height: 100%;background: url(../image/download.png) no-repeat center;background-size: 60%;"></a>');

    //   var iframe = window.parent.document.querySelector('#container');
  //   var currentpath = window.location.href;
  //   if (iframe) {
  //     currentpath = iframe.src;
  //   }
  //   if (currentpath.indexOf("html") < 0) {
  //     var u =
  //       "https://www.esmap.cn/escopemap/content/cn/develope/map-download.html";
  //     var str = currentpath.match(/demo\/.*?\//)[0];
  //     str = str.slice(5, -1); // demo所在文件夹的名称
  //     switch (str) {
  //       case "BaseMap":
  //         u += "#m_base";
  //         break;
  //       case "HeatMap":
  //         u += "#m_heatMap";
  //         break;
  //       case "Widgets":
  //         u += "#m_widgets";
  //         break;
  //       case "Effects":
  //         u += "#m_effects";
  //         break;
  //       case "RouteAnalyser":
  //         u += "#m_route";
  //         break;
  //       case "Search":
  //         u += "#m_search";
  //         break;
  //       case "Events":
  //         u += "#m_events";
  //         break;
  //       case "vip":
  //           u += "#m_vip";
  //           break;
  //       case "Case":
  //             u += "#m_case";
  //             break;
  //       }
  //     ckCode(u, true);
  //   } else {
  //     var u =
  //       "https://www.esmap.cn/escopemap/content/cn/develope/map-download.html";
  //     var str = currentpath.match(/demo\/.*?\//)[0];
  //     str = str.slice(5, -1); // demo所在文件夹的名称
  //     switch (str) {
  //       case "BaseMap":
  //         u += "#m_base";
  //         break;
  //       case "HeatMap":
  //         u += "#m_heatMap";
  //         break;
  //       case "Widgets":
  //         u += "#m_widgets";
  //         break;
  //       case "Effects":
  //         u += "#m_effects";
  //         break;
  //       case "RouteAnalyser":
  //         u += "#m_route";
  //         break;
  //       case "Search":
  //         u += "#m_search";
  //         break;
  //       case "Events":
  //         u += "#m_events";
  //         break;
  //         case "vip":
  //           u += "#m_vip";
  //           break;
  //           case "Case":
  //             u += "#m_case";
  //             break;
  //     }
  //     ckCode(u, false);
  //   }
  };
})();
