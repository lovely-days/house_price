
// map

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
    
// Remov Layers

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
    RemoveAllLayer()
    
    $("#data_show_control_label").attr("class","nav-link")
    $("#condition_select_control_label").attr("class","nav-link")
    $("#data_analysis_control_label").attr("class","nav-link")
    $("#data_predict_control_label").attr("class","nav-link")

    $("#data_analysis_control_card").css("display", "none")
    $("#data_show_control_card").css("display","none")

    if ($("#data_select_control_label").attr("class") == "nav-link")
    {
        $("#data_select_control_label").attr("class", "nav-link active")
        setTimeout(()=>{$("#data_select_control_card").css("display", "block")} ,500)
    }
    else
    {
        $("#data_select_control_label").attr("class","nav-link")
        $("#data_select_control_card").css("display","none")
        
    }
}

function DataSelectRequest()
{
    $("#data_select_control_card").css("display","none")
    var status = $("#data_select_operator").val()

    //实例化一个矢量图层 Vector 作为绘制层
    var source = new ol.source.Vector()
    var drawlayer = new ol.layer.Vector({
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
    })

    switch (status) {
        case 'Clear':
            RemoveAllLayer()

            $("#data_select_operator").attr("value", "Rectangle")
            $("#data_select_control_label").attr("class","nav-link")
            return 0
            
        case 'Rectangle':
            drawtype = 'Circle';
            geometryFunction = ol.interaction.Draw.createBox();

            draw = new ol.interaction.Draw({
                source: source,
                type: drawtype,
                geometryFunction: geometryFunction
            });
            break;
            
        case 'Circle':
            drawtype = 'Circle'

            draw = new ol.interaction.Draw({
                source: source,
                type: drawtype,
            });
            break;
            
        case 'Polygon':
            drawtype = 'Polygon'

            draw = new ol.interaction.Draw({
                source: source,
                type: drawtype,
            });
            break;
            
        default:
            alert("错误输入，请重试!")

        }

    map.addInteraction(draw);

    // 绘制完成
    draw.on('drawend', function (e) {

        // 显示绘制图形
        map.addLayer(drawlayer)

        // 清空画笔
        if (draw) {
            map.removeInteraction(draw)
            draw=null          
        }

        // 获取关键信息并封装

        //封装结构

        // Circle : [[longitude,Latitude],[longitude,Latitude],radius] ,圆心坐标, 边界点坐标, 半径, 解决测地线精度不统一问题
        // Rectangle : [[longitude,Latitude],[longitude,Latitude]]
        // polygon : [[longitude,longitude],...,[-1,-1]] ,最后点与首点坐标相同

        select_condition = []

        // 图形关键信息获取

        geometry = e.feature.getGeometry()

        switch (status) {
            case 'Circle':
                const center = ol.proj.transform(geometry.getCenter(), 'EPSG:3857', 'EPSG:4326')
                const border = ol.proj.transform(geometry.getLastCoordinate(), 'EPSG:3857', 'EPSG:4326')
                const radius = geometry.getRadius()

                // 利用地图单位求得 km 制下圆半径
                let metersPerUnit = map.getView().getProjection().getMetersPerUnit()
                const km_radius = radius / (metersPerUnit * 1000)

                // alert(center[0])
                // alert(radius)
                // alert(km_radius)

                select_condition[0] = [center[0],center[1]]
                select_condition[1] = [border[0],border[1]]
                select_condition[2] = [km_radius]

                break;
            
            case 'Rectangle':
                const rec_coordinates = geometry.getCoordinates()

                const l_t_coordinate = ol.proj.transform(rec_coordinates[0][0], 'EPSG:3857', 'EPSG:4326')
                const r_b_coordinate = ol.proj.transform(rec_coordinates[0][2], 'EPSG:3857', 'EPSG:4326')

                select_condition[0] = [l_t_coordinate[0], l_t_coordinate[1]]
                select_condition[1] = [r_b_coordinate[0],r_b_coordinate[1]]
                
                break;
            
            case 'Polygon':
                const pol_coordinates = geometry.getCoordinates()
                console.log(pol_coordinates)

                const first_coordinate = ol.proj.transform(pol_coordinates[0][0], 'EPSG:3857', 'EPSG:4326')
                // alert(first_coordinate)

                for (item of pol_coordinates[0])
                {
                    count = 0
                    const every_coordinate = ol.proj.transform(item, 'EPSG:3857', 'EPSG:4326')

                    select_condition.push([every_coordinate[0], every_coordinate[1]])

                }
                // 终止条件 [-1, -1]
                select_condition.push([-1, -1])

                break;
            
            default:
                alert("错误输入，请重试!")
  
        }


        // ajax 提交

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
                // alert(JSON.stringify(response))
                if (JSON.stringify(response["features"]) == [])
                    alert("未找到该区域房源")
            
                var vectorSource = new ol.source.Vector({
                    features: (new ol.format.GeoJSON()).readFeatures(response,{
                        dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'
                    })
                });

                var DataSelect = new ol.layer.Vector({
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

                $("#data_select_control_label").attr("class", "nav-link")
                map.addLayer(DataSelect);

                Select_Feature()
                
            },
        error: function(request, textStatus, errorThrown) {
            alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            }
        });


    })



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
            //alert(JSON.stringify(response))
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

            Select_Feature()

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
            type: 'data_analysis',
            analysis_type: 'heat_map',
        }),
        heads : {
            'content-type' : 'application/json;charset=UTF-8'
        },
        dataType: 'json',
            success: function (response) {
            
            var vectorSource = new ol.source.Vector({
                features: (new ol.format.GeoJSON()).readFeatures(response,{
                    dataProjection : 'EPSG:4326',featureProjection : 'EPSG:3857'})});
            
            // Heatmap 热力图绘制
            var HeatMap = new ol.layer.Heatmap({
                source: vectorSource,
                blur: 10,
                radius: 3,
            });

            // 清空原图层
            RemoveAllLayer()
            // 热力图图层添加
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
            type: 'data_analysis',
            analysis_type: 'predict_interpolation_map',
        }),
        heads : {
            'content-type' : 'application/json;charset=UTF-8'
        },
        dataType: 'json',
        success: function (response) {
            
            // 预测房价点坐标数据
            longitude = response["longitude"]
            latitude = response["latitude"]
            price = response["price"]
            
            // 克里金插值参数设置
            let params={
                mapCenter:[117,34],
                maxValue:100,
                krigingModel:'exponential', // 'exponential':指数  'gaussian':高斯,'spherical':球体
                krigingSigma2:0,
                krigingAlpha:100,
                canvasAlpha:0.7, //canvas图层透明度
                colors:[
                    "#006837",
                    "#1a9850",
                    "#66bd63",
                    "#a6d96a",
                    "#d9ef8b",
                    "#ffffbf",
                    "#fee08b",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026"
                ],
            };

            // 克里金插值训练
            let variogram=kriging.train(price,longitude,latitude,params.krigingModel,params.krigingSigma2,params.krigingAlpha);
            let polygons=[[[117,34.1],[117,34.4],[117.4,34.4],[117.4,34.1]]];
            let grid = kriging.grid(polygons, variogram, (117.4 - 117) / 800);
                
            // 创建新图层
            canvasLayer=new ol.layer.Image({
                source: new ol.source.ImageCanvas({
                    canvasFunction:(extent, resolution, pixelRatio, size, projection) =>{
                        let canvas = document.createElement('canvas');
                            canvas.width = size[0];
                            canvas.height = size[1];
                            canvas.style.display='block';
                            //设置canvas透明度
                            canvas.getContext('2d').globalAlpha=params.canvasAlpha;                          
                            //使用分层设色渲染
                        kriging.plot(canvas,grid,[extent[0],extent[2]],[extent[1],extent[3]],params.colors);
                            return canvas;
                    },
                projection: 'EPSG:4326'
                })
                    
            })

            // 清空原图层
            RemoveAllLayer()
            // 向map添加图层
            map.addLayer(canvasLayer);
         
        },
        error: function(request, textStatus, errorThrown) {
            alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            }
        });
    }
    else
    {
        RemoveAllLayer()
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

// Feature select

function Select_Feature()
{
    if (selectClick)
    {
        map.removeInteraction(selectClick)
        selectClick = null
    }

    // 选择控件创建与添加
    var selectClick = new ol.interaction.Select();
    map.addInteraction(selectClick);
    
    /*
    // 逻辑太复杂了，boom 。。
    // 绑定点击事件获取绝对坐标，设置模态框位置
    $('body').on('click', function (ex) {
        if (ex == null) {
            ex = window.event;
        }

        right_val = (parseInt(ex.clientX) - 100).toString() + 'px'
        top_val = (parseInt(ex.clientY) - 100).toString() + 'px'
        // alert(right_val)
        // alert(top_val)

        // 属性展示模态框显示
        $("#feature_show_content").css("right", right_val)
        $("#feature_show_content").css("top", top_val)
        $('body').off('click')
    })
    */

    // 地图选择要素
    selectClick.on('select', function (e) {
        
        var features=e.target.getFeatures().getArray();
        if (features.length > 0) {
            var property = features[0].getProperties();

            // 添加属性表项
            for (key in property)
            {
                value = property[key]

                if (key == 'geometry' || key == 'Coordinate' || key == 'House ID')
                    continue

                if (key == 'Price')
                    value = value + '万元'
                
                if (key == 'Unit Price')
                    value = value + '元'
                
                /*
                    <tr>
                        <th scope="col">属性名</th>
                        <th scope="col">属性值</th>
                    </tr>
                */
                
                line = '<tr> <th scope="col">' + key +'</th> <th scope="col"><th>' + value + '</th> </tr>' 
                // console.log(line)

                //alert(line)

                $('#feature_column').append(line)
            }

            // 显示修改后模态框
            $("#feature_show").css("display", "block")

            selectClick.off()
            
        }   
    })

}

function featureSelectClose()
{
    //  关闭模态框
    $("#feature_show").css("display", "none")
    $("#feature_column").empty()
}
