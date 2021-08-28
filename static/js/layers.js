/////////////// Geoserver中发布的  House 信息 ///////////////
var  House = new ol.layer.Image({
                    source:new ol.source.ImageWMS({
                        // http://localhost:8080/geoserver/WebGIS/wms
                        url:'http://localhost:8080/geoserver/GIS/wms',
                        params:{'LAYERS':'class:House'},
                        serverType: 'geoserver',
                        visible: false
                    })                    
                });

/////////////// Geoserver中发布的 Hospital 信息 ///////////////
var Hospital = new ol.layer.Image({
                    source:new ol.source.ImageWMS({
                        url:'http://localhost:8080/geoserver/GIS/wms',
                        params:{'LAYERS':'class:Hospital'},
                        serverType: 'geoserver',
                        visible: false
                    })
                });

/////////////// Geoserver中发布的 School 信息 ///////////////
var School = new ol.layer.Image({
                    source:new ol.source.ImageWMS({
                        url:'http://localhost:8080/geoserver/GIS/wms',
                        params:{'LAYERS':'class:School'},
                        serverType: 'geoserver',
                        visible: false                        
                    })
                });

/////////////// Geoserver中发布的 Environment 信息 ///////////////
var Environment = new ol.layer.Image({
                    source:new ol.source.ImageWMS({
                        url:'http://localhost:8080/geoserver/GIS/wms',
                        params:{'LAYERS':'class:Environment'},
                        serverType: 'geoserver',
                        visible: false                        
                    })
                });

/////////////// Geoserver中发布的 Subway 信息 ///////////////
var Subway = new ol.layer.Image({
                    source:new ol.source.ImageWMS({
                        url:'http://localhost:8080/geoserver/GIS/wms',
                        params:{'LAYERS':'class:Sub'},
                        serverType: 'geoserver',
                        visible: false                        
                    })
                });

/////////////// Geoserver中发布的 Bus_station 信息 ///////////////
var Bus_station = new ol.layer.Image({
                    source:new ol.source.ImageWMS({
                        url:'http://localhost:8080/geoserver/GIS/wms',
                        params:{'LAYERS':'class:BusStops'},
                        serverType: 'geoserver',
                        visible: false
                    })
                });

/////////////// Geoserver中发布的 Shopping 信息 ///////////////
var Shopping = new ol.layer.Image({
                    source:new ol.source.ImageWMS({
                        url:'http://localhost:8080/geoserver/GIS/wms',
                        params:{'LAYERS':'class:Shopping'},
                        serverType: 'geoserver',
                        visible: false
                    })
                });


