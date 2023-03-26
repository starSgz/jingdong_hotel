
$(function () {
    map();
    function map() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('map'));
        var url = "/map";
        // var data=[{name: '海门', value: 9}]
        // var geoCoordMap={'海门':[121.15,31.89]}
		$.ajax({
			url: url,
			type: "GET",
			data: {},
			dataType: 'JSON',
			success: function (req) {
				console.log(req);
                var data= req.data.data;
                var geoCoordMap = req.data.geoCoordMap

                var convertData = function (data) {
                    var res = [];
                    for (var i = 0; i < data.length; i++) {
                        var geoCoord = geoCoordMap[data[i].name];
                        if (geoCoord) {
                            res.push({
                                name: data[i].name,
                                value: geoCoord.concat(data[i].value)
                            });
                        }
                    }
                    return res;
                };
                console.log(convertData(data))
                option = {
                    // backgroundColor: '#404a59',
                   title: {
                         text: '酒店数量分布',
                         left: 'center',
                         top:'40',
                         textStyle: {
                             color: '#fff'
                         }
                     },
                     tooltip : {
                        show: true,
                        trigger: 'item',

                        formatter: function (e) {
                            console.log(e)
                            return e.name + '：' + e.value[2]+"家"
                        }
    

                     },
                   
                     geo: {
                         map: 'china',
                         label: {
                             emphasis: {
                                 show: false
                             }
                         },
                         roam: false,
                         zoom:1.2,
                         itemStyle: {
                             normal: {
                                 areaColor: 'rgba(2,37,101,.5)',
                                 borderColor: 'rgba(112,187,252,.5)'
                             },
                             emphasis: {
                                 areaColor: 'rgba(2,37,101,.8)'
                             }
                         }
                     },
                     series : [
                         {
                             name: '数量',
                             type: 'scatter',
                             coordinateSystem: 'geo',
                             data: convertData(data),
                             symbolSize: function (val) {
                                 return val[2] / 15;
                             },
                             label: {
                                 normal: {
                                     formatter: '{a}',
                                     position: 'right',
                                     show: false
                                 },
                                 emphasis: {
                                     show: true
                                 }
                             },
                             itemStyle: {
                                 normal: {
                                     color: '#ffeb7b'
                                 }
                             }
                         }
                 
                     ]
                 };
                 myChart.setOption(option);
                 window.addEventListener("resize",function(){
                     myChart.resize();
                 });
			}
		});
	
    }

})

