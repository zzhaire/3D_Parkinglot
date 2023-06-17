/////////////////////////////////////////////////////////
/////////////封装右边图层控制控件代码----开始/////////////
/////////////////////////////////////////////////////////
var gui = {};

gui.showModelInfo = function (d) {
  //console.log(d);
  $("#dlgModelInfo").modal("show");
  $("#dlgModelInfo .modal-title").text("模型名称：" + d.name);
  $("#dlgModelInfo #m-fnum").text(d.fnum);
  $("#dlgModelInfo #m-ID").text(d.ID);
  $("#dlgModelInfo #m-type").text(d.type);
  $("#dlgModelInfo #m-x").text(d.x);
  $("#dlgModelInfo #m-y").text(d.y);
};

gui.showLabelInfo = function (d) {
  //console.log(d);
  $("#dlgLabellInfo").modal("show");
  $("#dlgLabellInfo .modal-title").text("label名称：" + d.name);
  $("#dlgLabellInfo #l-fnum").text(d.fnum);
  $("#dlgLabellInfo #l-ID").text(d.ID);
  $("#dlgLabellInfo #l-x").text(d.x);
  $("#dlgLabellInfo #l-y").text(d.y);
};

gui.showPOIInfo = function (d) {
  //console.log(d);
  $("#dlgPOIInfo").modal("show");
  $("#dlgPOIInfo .modal-title").text("poi名称：" + d.name);
  $("#dlgPOIInfo #p-fnum").text(d.fnum);
  $("#dlgPOIInfo #p-ID").text(d.ID);
  $("#dlgPOIInfo #p-x").text(d.x);
  $("#dlgPOIInfo #p-y").text(d.y);
};
gui.showListInfo = function (d) {
  $(".container-fluid").empty();
  $("#dlgListInfo").modal("show");

  for (var i = 0; i < d.length; i++) {
    var e = d[i];
    var typename = "对象";
    switch (e.nodeType) {
      case esmap.ESNodeType.MODEL:
        typename = "房间";
        break;
      case esmap.ESNodeType.MODEL3D:
        typename = "三维模型";
        break;
      case esmap.ESNodeType.IMAGE_MARKER:
        typename = "图片标注";
        break;
      case esmap.ESNodeType.TEXT_MARKER:
        typename = "文字标注";
        break;
      case esmap.ESNodeType.FACILITY:
        typename = "POI";
        break;
    case esmap.ESNodeType.LABEL:
        typename = "LABEL";
        break;
    }

    var temp = `
        <div class="row">
            <div class="col-md-6">名称 ${e.name || e.model}</div>
            <div class="col-md-3">类型 ${typename}</div>
            <div class="col-md-3" id="p-fnum">楼层 ${e.FloorNum}</div>
        </div>
        `;
    $(".container-fluid").append(temp);
  }
};

/////////////////////////////////////////////////////////
/////////////封装右边图层控制控件代码----结束////////////
/////////////////////////////////////////////////////////
