//const layers = require("./layers");

     var map = new ol.Map({
        target: 'map',                          // 关联到对应的div容器
        layers: [
            new ol.layer.Tile({                 // 瓦片图层
                source: new ol.source.OSM()     // OpenStreetMap数据源
            }),
        ],
        view: new ol.View({                     // 地图视图
            projection: 'EPSG:3857',
            center: ol.proj.fromLonLat([117.200931, 34.219325]),
            zoom: 14,
        })
});

    map.addControl(new ol.control.FullScreen())
    map.addControl(new ol.control.ScaleLine())
    map.addControl(new ol.control.ZoomSlider())
    
 


    /*
    map.on('singleclick', function(e){
		alert(e.coordinate);
		alert(ol.proj.transform(e.coordinate, 'EPSG:3857', 'EPSG:4326'));

        // 通过getEventCoordinate方法获取地理位置，再转换为wgs84坐标，并弹出对话框显示
		alert(map.getEventCoordinate(e.originalEvent));
        alert(ol.proj.transform(map.getEventCoordinate(e.originalEvent), 'EPSG:3857', 'EPSG:4326'));

        var lonlat = map.getCoordinateFromPixel(e.pixel);
		alert(lonlat);
        alert(ol.proj.transform(lonlat,"EPSG:3857", "EPSG:4326")); //由3857坐标系转为4326
　　　　
    })

    $("singleclick").off("click")
    */

function RemoveAllLayer()
{
    map.setLayerGroup(new ol.layer.Group())
    map.addLayer(new ol.layer.Tile({ source: new ol.source.OSM() }))
}

// Data Show

function OpenDataShowCard()
{
    $("#data_select_control_label").attr("class","nav-link")
    $("#condition_select_control_label").attr("class","nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")
    $("#data_predict_control_label").attr("class","nav-link")

    $("#data_analysis_control_card").css("display","none")

    if ($("#data_show_control_label").attr("class") == "nav-link")
    {
        $("#data_show_control_label").attr("class","nav-link active")
        $("#data_show_control_card").css("display","block")  
    }
    else
    {
        $("#data_show_control_label").attr("class","nav-link")
        $("#data_show_control_card").css("display","none")
        
    }
}

function DataShow()
{
    RemoveAllLayer()

    if($("#house_check").prop("checked"))
    {
        map.addLayer(House)
        alert(1)
    }

    if($("#hospital_check").prop("checked"))
    { 
        map.addLayer(Hospital)
        alert(2)
    }

    if($("#school_check").prop("checked"))
    {
        map.addLayer(School)
        alert(3)
    }

    if($("#environment_check").prop("checked"))
    {
        map.addLayer(Environment)
        alert(4)
    }

    if($("#subway_check").prop("checked"))
    {
        map.addLayer(Subway)
        alert(5)
    }

    if($("#bus_station_check").prop("checked"))
    {
        map.addLayer(Bus_station)
        alert(6)
    }

    if($("#shopping_check").prop("checked"))
    {
        map.addLayer(Shopping)
        alert(7)
    }

}

function CheckOrCancelAll()
{
    var items=["#house_check","#hospital_check","#school_check","#environment_check","#subway_check","#bus_station_check","#shopping_check"]

    if ($("#all_check").prop("checked"))
    {
       
        for (var i = 0; i < items.length;i++)
        {
            $(items[i]).prop("checked", true)
        }
        
    }
    else
    {  
        for (var i = 0; i < items.length;i++)
        {
            $(items[i]).prop("checked", false)
        }
    }
}

// Data Select

function OpenDataSelectCard()
{
    
    $("#data_show_control_label").attr("class","nav-link")
    $("#condition_select_control_label").attr("class","nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")
    $("#data_predict_control_label").attr("class","nav-link")

    $("#data_analysis_control_card").css("display","none")

    if ($("#data_select_control_label").attr("class") == "nav-link")
    {
        $("#data_select_control_label").attr("class","nav-link active")
        $("#data_select_control_card").css("display","block")  
    }
    else
    {
        $("#data_select_control_label").attr("class","nav-link")
        $("#data_select_control_card").css("display","none")
        
    }
}

function DataSelectRequest()
{
    alert(1)
    RemoveAllLayer()
    var status = $("#data_select_operator").val()
    alert(status)

    if (status == 'None')
    {
        alert(1)
    }
    else if (status == 'Point')
    {                               
        alert(2)
    }
    else if (status == 'LineString')
    {
        alert(3)
    }
    else if (status == 'Square')
    {
        alert(4)       
    }
    else if (status == 'Polygon')
    {
        alert(5)
    }
    else if (status == 'Circle')
    {
        alert(6)        
    }
    else
    {
        alert("1") 
    }

    select_condition = []

    // ajax 提交

    /*
        $.ajax({
        type: 'POST',
        data: JSON.stringify({
            type: 'data_select',
            select_type:status,
            select_condition:select_condition
        }),
        heads : {
            'content-type' : 'application/json;charset=UTF-8'
        },
        dataType: 'json',
        success: function (response) {
                # 返回操作
            },
        error: function(request, textStatus, errorThrown) {
            alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            }
        });




    */

}

function DataSelectModalClose()
{
    $("#data_select_control_label").attr("class", "nav-link")
    $("#data_select_control_card").css("display", "none")
}

// Condition Select

function OpenConditionSelectCard() {
    RemoveAllLayer()

    $("#data_show_control_label").attr("class","nav-link")
    $("#data_select_control_label").attr("class", "nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")
    $("#data_predict_control_label").attr("class","nav-link")

    $("#data_show_control_card").css("display","none")
    $("#data_analysis_control_card").css("display", "none")

    if ($("#condition_select_control_label").attr("class") == "nav-link")
    {
        $("#condition_select_control_label").attr("class", "nav-link active")   
        setTimeout(()=>{$("#condition_select_control_card").css("display", "block")} ,500)
    }
    else
    {
        $("#condition_select_control_label").attr("class", "nav-link")
        $("#condition_select_control_card").css("display", "none")

    }
}

function ConditionSelectRequest() {
    $.ajax({
        type: 'POST',
        data: JSON.stringify({
            type: 'condition_select',
            region: $("#condition_region").val(),
            roomtype: $("#condition_roomtype").val(),
            area: $("#condition_area").val(),
            all_price: $("#condition_all_price").val(),
            unit_price: $("#condition_unit_price").val(),
            direction: $("#condition_direction").val(),
            floor: $("#condition_floor").val(),
            house_type: $("#condition_house_type").val()   
        }),
        heads : {
            'content-type' : 'application/json;charset=UTF-8'
        },
        dataType: 'json',
        success: function (response) {
            alert(JSON.stringify(response))
            if (JSON.stringify(response["features"]) == [])
                alert("未找到该条件下房源")
            
            var vectorSource = new ol.source.Vector({
                features: (new ol.format.GeoJSON()).readFeatures(response,{
                    dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'
                })
            });

            var ConditionSelect = new ol.layer.Vector({
	            source: vectorSource,
	            style:new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 5,//半径
                        fill: new ol.style.Fill({//填充样式
                            color: '#ff6688',
                        }),
                        stroke: new ol.style.Stroke({//边界样式
                            color: '#555555',
                            width: 1
                        })
                    }),
                })
            });

            $("#condition_select_control_label").attr("class", "nav-link")
            $("#condition_select_control_card").css("display", "none")
            map.addLayer(ConditionSelect);
            },
        error: function(request, textStatus, errorThrown) {
            alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            }
        });

}

function ConditionSelectModalClose(){
    $("#condition_select_control_label").attr("class", "nav-link")
    $("#condition_select_control_card").css("display", "none")
}

// Data Analysis

function OpenDataAnalysisCard()
{
    RemoveAllLayer()

    $("#data_show_control_label").attr("class","nav-link")
    $("#data_select_control_label").attr("class", "nav-link")
    $("#condition_select_control_label").attr("class","nav-link")
    $("#data_predict_control_label").attr("class","nav-link")

    $("#data_show_control_card").css("display","none")

    if ($("#data_analysis_control_label").attr("class") == "nav-link")
    {
        $("#data_analysis_control_label").attr("class","nav-link active")
        $("#data_analysis_control_card").css("display","block")
    }
    else
    {
        $("#data_analysis_control_label").attr("class","nav-link")
        $("#data_analysis_control_card").css("display","none")

    }

}

function heat_map()
{
    if($("#heat_map").prop("checked"))
    {
        $.ajax({
        type: 'POST',
        data: JSON.stringify({
            type: 'heat_map',
        }),
        heads : {
            'content-type' : 'application/json;charset=UTF-8'
        },
        dataType: 'json',
        success: function(response) {
            var vectorSource = new ol.source.Vector({
                features: (new ol.format.GeoJSON()).readFeatures(response,{
                    dataProjection : 'EPSG:4326',featureProjection : 'EPSG:3857'})});
                // Heatmap热力图
            var HeatMap = new ol.layer.Heatmap({
                source: vectorSource,
                blur: 10,
                radius: 3,
            });
            map.addLayer(HeatMap);
            },
        error: function(request, textStatus, errorThrown) {
            alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            }
        });
    }
    else
    {
        map.removeLayer(vector)
    }

}

function predict_interpolation_map()
{
    if($("#predict_interpolation_map").prop("checked"))
    {
        $.ajax({
        type: 'POST',
        data: JSON.stringify({
            type: 'predict_interpolation_map',
        }),
        heads : {
            'content-type' : 'application/json;charset=UTF-8'
        },
        dataType: 'json',
        success: function(response) {
            var vectorSource = new ol.source.Vector({
                features: (new ol.format.GeoJSON()).readFeatures(response,{
                    dataProjection : 'EPSG:4326',featureProjection : 'EPSG:3857'})});
                // Heatmap热力图
            var HeatMap = new ol.layer.Heatmap({
                source: vectorSource,
                blur: 10,
                radius: 3,
            });
            map.addLayer(HeatMap);
            },
        error: function(request, textStatus, errorThrown) {
            alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            }
        });
    }
    else
    {
        map.removeLayer(vector)
    }
}

function other_map()
{
    RemoveAllLayer()
}

function analysis_remove()
{
    RemoveAllLayer()
}

// Data Predict

function DataPredict()
{
    RemoveAllLayer()

    $("#data_show_control_label").attr("class","nav-link")
    $("#data_select_control_label").attr("class", "nav-link")
    $("#condition_select_control_label").attr("class","nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")

    $("#data_show_control_card").css("display","none")
    $("#data_analysis_control_card").css("display","none")

    if ($("#data_predict_control_label").attr("class") == "nav-link")
    {
        $("#data_predict_control_label").attr("class", "nav-link active")
        setTimeout(()=>{alert("请选择预测位置")} ,500)

        $("#map").on('click', function(e){
        var coordinate = ol.proj.transform(map.getEventCoordinate(e.originalEvent), 'EPSG:3857', 'EPSG:4326')

        $.ajax({
        type: 'POST',
        data: JSON.stringify({
            type: "house_predict",
            coordinates: [coordinate[0],coordinate[1]],
        }),
        heads : {
            'content-type' : 'application/json;charset=UTF-8'
        },
        dataType: 'json',
        success: function(response) {
            alert("该处预测单位房价为 " + response["predict"] + " 元每平米")
            $("#data_predict_control_label").attr("class","nav-link")
            $("#map").off("click")
            },
        error: function(request, textStatus, errorThrown) {
            alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            $("#map").off("click")
            }
        });
    })

    }
    else
    {
        $("#data_predict_control_label").attr("class","nav-link")
    }
}


function addInteraction() {

         var typeSelect = document.getElementById('type');       //绘制类型选择对象

      //ol.Interaction.Draw类的对象
      var draw;

      //实例化一个矢量图层Vector作为绘制层
      var source = new ol.source.Vector();
      var vectorLayer = new ol.layer.Vector({
          source: source,
          style: new ol.style.Style({
              fill: new ol.style.Fill({               //填充样式
                  color: 'rgba(255, 255, 255, 0.2'
              }),
              stroke: new ol.style.Stroke({           //线样式
                  color: '#00c033',
                  width: 2
              }),
              image: new ol.style.Circle({            //点样式
                  radius: 7, 
                  fill: new ol.style.Fill({
                      color: '#00c033'
                  })
              })
          })
      });
      //将绘制层添加到地图容器中
      map.addLayer(vectorLayer);           

      //用户更改绘制类型触发的事件
     
      typeSelect.onchange = function(e){
          map.removeInteraction(draw);        //移除绘制图形控件
          addInteraction();                   //添加绘制图形控件
      }; 

          var typeValue = typeSelect.value;       //绘制类型
          
          if(typeValue !== 'None'){
              var geometryFunction, maxPoints;
              if(typeValue === 'Square'){                 //正方形
                  typeValue = 'Circle';               //设置绘制类型为Circle
                  //设置几何信息变更函数，即创建正方形
                  geometryFunction = ol.interaction.Draw.createRegularPolygon(4);
              }
              console.log(typeValue);
              //实例化图形绘制控件对象并添加到地图容器中
              draw = new ol.interaction.Draw({
                  source: source,
                  type: typeValue,                                //几何图形类型
                  geometryFunction: geometryFunction,             //几何信息变更时的回调函数
                  maxPoints: maxPoints                            //最大点数
              });
              map.addInteraction(draw);
          }else{
              //清空绘制的图形
              source.clear();
          }
      }

