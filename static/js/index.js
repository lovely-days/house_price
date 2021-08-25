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

// DataShowCard

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
    //map.removeLayer(House)
    //map.removeLayer(Hospital)
    //map.removeLayer(School)
    //map.removeLayer(Environment)
    //map.removeLayer(Subway)
    //map.removeLayer(Bus_station)
    //map.removeLayer(Shopping)

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

function OpenDataSelectCard()
{
    $("#data_show_control_label").attr("class","nav-link")
    $("#condition_select_control_label").attr("class","nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")
    $("#data_predict_control_label").attr("class","nav-link")

    $("#data_show_control_card").css("display","none")
    $("#data_analysis_control_card").css("display","none")

    if ($("#data_select_control_label").attr("class") == "nav-link")
    {
            $("#data_select_control_label").attr("class", "nav-link active")
    }
    else
    {
        $("#data_select_control_label").attr("class","nav-link")

    }
}

function OpenConditionSelectCard(){
    $("#data_show_control_label").attr("class","nav-link")
    $("#data_select_control_label").attr("class", "nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")
    $("#data_predict_control_label").attr("class","nav-link")

    $("#data_show_control_card").css("display","none")
    $("#data_analysis_control_card").css("display", "none")

    if ($("#condition_select_control_label").attr("class") == "nav-link")
    {
        $("#condition_select_control_label").attr("class", "nav-link active")
        $("#condition_select_control_card").css("display", "block")
    }
    else
    {
        $("#condition_select_control_label").attr("class", "nav-link")
        $("#condition_select_control_card").css("display", "none")

    }
}

function OpenDataAnalysisCard()
{
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
            var vector = new ol.layer.Heatmap({
                source: vectorSource,
                blur: 10,
                radius: 3,
            });
            map.addLayer(vector);
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

function DataPredict()
{
    $("#data_show_control_label").attr("class","nav-link")
    $("#data_select_control_label").attr("class", "nav-link")
    $("#condition_select_control_label").attr("class","nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")

    $("#data_show_control_card").css("display","none")
    $("#data_analysis_control_card").css("display","none")

    if ($("#data_predict_control_label").attr("class") == "nav-link")
    {
        $("#data_predict_control_label").attr("class","nav-link active")
        alert("请选择预测位置")

        $("#map").on('click', function(e){
        var coordinate = ol.proj.transform(map.getEventCoordinate(e.originalEvent), 'EPSG:3857', 'EPSG:4326')
        alert(coordinate)
        alert(coordinate[0])
        alert(coordinate[1])

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

