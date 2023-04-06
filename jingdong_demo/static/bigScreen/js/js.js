$(window).load(function () {
    $(".loading").fadeOut()
})
$(function () {
    map();
    echarts_2()
    echarts_3() //数量Top10的品牌酒店的均价
    echarts_4()
    echarts_5()
    echarts_6()

    var myChart1;
    var myChart2;
    var myChart3;
    var myChart4;
    var myChart5;
    var myChart6;

    // 定义触发器
    myChart1.on('click', function (params) {
            console.log(params["name"]);
            echarts_2("cityName", cityName = params["name"]) //品牌数量Top15
            echarts_3("cityName", cityName = params["name"])
            echarts_4("cityName", cityName = params["name"])
            echarts_5("cityName", cityName = params["name"])
            echarts_6("cityName", cityName = params["name"])
            request_dataStatistics("cityName",params["name"])

        }); //中国地图
    myChart2.on('click', function (params) {
            console.log(params);
            map("brandName", brandName = params["name"]);
            echarts_3("brandName", brandName = params["name"])
            echarts_4("brandName", brandName = params["name"])
            echarts_5("brandName", brandName = params["name"])
            echarts_6("brandName", brandName = params["name"])
            request_dataStatistics("brandName",params["name"])
        });//品牌数量Top15
    myChart3.getZr().on('click', function (params) {
            console.log(params);
        });//数量Top10的品牌酒店的均价
    myChart4.on('click', function (params) {
            console.log(params);
            map("businessZoneName", businessZoneName = params["name"]);
            echarts_2("businessZoneName", businessZoneName = params["name"])
            echarts_3("businessZoneName", businessZoneName = params["name"])
            echarts_5("businessZoneName", businessZoneName = params["name"])
            echarts_6("businessZoneName", businessZoneName = params["name"])
            request_dataStatistics("businessZoneName",params["name"])

        });//商圈Top8
    myChart5.on('click', function (params) {
            console.log(params);
            map("grade", grade = params["name"]);
            echarts_2("grade", grade = params["name"])
            echarts_3("grade", grade = params["name"])
            echarts_4("grade", grade = params["name"])
            echarts_6("grade", grade = params["name"])
            request_dataStatistics("grade",params["name"])

        });//星级占比
    myChart6.on('click', function (params) {
            console.log(params);
        });//设施配备
    //请求统计信息
    function request_dataStatistics(keys,values) {
        $.ajax({
            url: "/dataStatistics?"+keys+"=" + values,
            type: 'GET',
            success: function (data) {
                // 根据id修改标签里面的文本内容
                console.log(data.data.allcount)
                //修改文本
                $("#allcounName").text(data.screeningCondition + "酒店总数量");
                var hotelMax = data.data.hotelMax;
                var hotelMaxKeys = Object.keys(hotelMax);
                for (var i = 0; i < hotelMaxKeys.length; i++) {
                    var key = hotelMaxKeys[i];
                    $("#hotelMaxName").text("最多酒店的城市:" + key);
                }
                //修改数字
                $("#allcount").text(data.data.allcount);
                $("#avgScore").text(data.data.avgScore);
                $("#brandNum").text(data.data.brandNum);
                for (var i = 0; i < hotelMaxKeys.length; i++) {
                    var key = hotelMaxKeys[i];
                    var value = hotelMax[key];
                    $("#hotelMax").text(value);
                }
            },
            error: function () {
                console.log("请求失败！");
            }
        });
    }

    //中国地图
    function map(keys = "", condition = "全国") {
        // 基于准备好的dom，初始化echarts实例
        myChart1 = echarts.init(document.getElementById('map'));
        if (condition == "全国") {
            request_map("/map")//默认全国
        } else {
            url = "/map?" + keys + "=" + condition
            request_map(url)
        }
        function request_map(url) {
            $.ajax({
                url: url,
                type: "GET",
                data: {},
                dataType: 'JSON',
                success: function (req) {
                    console.log(req);
                    var data = req.data.data;
                    var geoCoordMap = req.data.geoCoordMap

                    var max = 0;
                    var min = Number.MAX_VALUE;
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].value > max) {
                            max = data[i].value;
                        }
                        if (data[i].value < min) {
                            min = data[i].value;
                        }
                    }

                    var size = function (val) {
                        return (val - min) / (max - min) * 50;
                    };

                    var convertData = function (data) {
                        var res = [];
                        for (var i = 0; i < data.length; i++) {
                            var geoCoord = geoCoordMap[data[i].name];
                            if (geoCoord) {
                                res.push({
                                    name: data[i].name,
                                    value: geoCoord.concat(data[i].value),
                                    symbolSize: size(data[i].value) // 修改点的大小
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
                            top: '40',
                            textStyle: {
                                color: '#fff'
                            }
                        },
                        tooltip: {
                            show: true,
                            trigger: 'item',
                            formatter: function (e) {
                                // console.log(e)
                                return e.name + '：' + e.value[2] + "家"
                            }
                        },
                        geo: {
                            map: 'china',
                            label: {
                                emphasis: {
                                    show: false
                                }
                            },
                            roam: true, // 开启缩放功能
                            zoom: 1.2,
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
                        series: [
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
                    myChart1.setOption(option);
                    window.addEventListener("resize", function () {
                        myChart.resize();
                    });
                }
            });
        }
    }

    //完成 品牌数量Top15
    function echarts_2(keys = "", condition = "全国") {
        // 基于准备好的dom，初始化echarts实例
        myChart2 = echarts.init(document.getElementById('echart2'));
        if (condition == "全国") {
            request_brand("/brandTop")//默认全国
        } else {
            url = "/brandTop?" + keys + "=" + condition
            request_brand(url)
        }


        function request_brand(url) {
            $.ajax({
                type: "GET",
                url: url,
                data: "{}",
                dataType: "JSON",
                success: function (response) {
                    var data = Object.values(response.data)
                    var titlename = Object.keys(response.data)
                    console.log(response.data)
                    option = {
                        grid: {
                            left: '0',
                            top: '0',
                            right: '0',
                            bottom: '0%',
                            containLabel: true
                        },
                        xAxis: {
                            show: false
                        },
                        yAxis: [{
                            show: true,
                            data: titlename,
                            inverse: true,
                            axisLine: {show: false},
                            splitLine: {show: false},
                            axisTick: {show: false},
                            axisLabel: {
                                textStyle: {
                                    color: '#fff'
                                },
                            },

                        }, {
                            show: false,
                            inverse: true,
                            data: data,
                            axisLabel: {textStyle: {color: '#fff'}},
                            axisLine: {show: false},
                            splitLine: {show: false},
                            axisTick: {show: false},
                        }],
                        series: [{
                            name: '条',
                            type: 'bar',
                            yAxisIndex: 0,
                            data: data,
                            barWidth: 15,
                            itemStyle: {
                                normal: {
                                    barBorderRadius: 50,
                                    color: '#1089E7',
                                }
                            },
                            label: {
                                normal: {
                                    show: true,
                                    position: 'right',
                                    formatter: '{c}',
                                    textStyle: {color: 'rgba(255,255,255,.5)'}
                                }
                            },
                        }]
                    };
                    // 使用刚指定的配置项和数据显示图表。
                    myChart2.setOption(option);
                    window.addEventListener("resize", function () {
                        myChart.resize();
                    });
                }
            });
        }
    }

    //数量Top10的品牌酒店的均价
    function echarts_3(keys = "", condition = "全国") {
        // 基于准备好的dom，初始化echarts实例
        myChart3 = echarts.init(document.getElementById('echart3'));
        if (condition == "全国") {
            request_brandAvgPrice("/brandAvgPrice")//默认全国
        } else {
            url = "/brandAvgPrice?" + keys + "=" + condition
            request_brandAvgPrice(url)
        }


        function request_brandAvgPrice(url) {
            $.ajax({
                type: "GET",
                url: url,
                data: "{}",
                dataType: "JSON",
                success: function (response) {
                    console.log(Object.keys(response.data))
                    option = {
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                lineStyle: {
                                    color: '#dddc6b'
                                }
                            }
                        },
                        grid: {
                            left: '10',
                            top: '20',
                            right: '30',
                            bottom: '10',
                            containLabel: true
                        },

                        xAxis: [{
                            type: 'category',
                            interval: 0,
                            boundaryGap: false,
                            axisLabel: {
                                rotate: 45,
                                textStyle: {
                                    color: "rgba(255,255,255,.6)",
                                    fontSize: 10,
                                },
                            },
                            axisLine: {

                                lineStyle: {
                                    color: 'rgba(255,255,255,.2)'
                                }

                            },
                            data: Object.keys(response.data)
                        }, {

                            axisPointer: {show: false},
                            axisLine: {show: false},
                            position: 'bottom',
                            offset: 20,
                        }],
                        yAxis: [{
                            type: 'value',
                            axisTick: {show: false},
                            splitNumber: 4,
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.1)'
                                }
                            },
                            axisLabel: {
                                textStyle: {
                                    color: "rgba(255,255,255,.6)",
                                    fontSize: 16,
                                },
                            },
                            splitLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.1)',
                                    type: 'dotted',
                                }
                            }
                        }],
                        series: [
                            {
                                name: '品牌酒店平均价格',
                                type: 'line',
                                smooth: true,
                                symbol: 'circle',
                                symbolSize: 5,
                                showSymbol: false,
                                lineStyle: {

                                    normal: {
                                        color: 'rgba(31, 174, 234, 1)',
                                        width: 2
                                    }
                                },
                                areaStyle: {
                                    normal: {
                                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: 'rgba(31, 174, 234, 0.4)'
                                        }, {
                                            offset: 0.8,
                                            color: 'rgba(31, 174, 234, 0.1)'
                                        }], false),
                                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                                    }
                                },
                                itemStyle: {
                                    normal: {
                                        color: '#1f7eea',
                                        borderColor: 'rgba(31, 174, 234, .1)',
                                        borderWidth: 5
                                    }
                                },
                                data: Object.values(response.data)
                            },
                        ]
                    };
                    // 使用刚指定的配置项和数据显示图表。
                    myChart3.setOption(option);
                    window.addEventListener("resize", function () {
                        myChart.resize();
                    });
                }
            });
        }

    }

    //商圈Top8
    function echarts_4(keys = "", condition = "全国") {
        // 基于准备好的dom，初始化echarts实例
        myChart4 = echarts.init(document.getElementById('echart4'));
        if (condition == "全国") {
            request_businessZone("/businessZone")//默认全国
        } else {
            url = "/businessZone?" + keys + "=" + condition
            request_businessZone(url)
        }


        function request_businessZone(url) {
            $.ajax({
                type: "GET",
                url: url,
                data: "{}",
                dataType: "JSON",
                success: function (response) {
                    var data = Object.values(response.data)
                    var titlename = Object.keys(response.data)
                    option = {
                        grid: {
                            left: '0',
                            top: '30',
                            right: '0',
                            bottom: '10',
                            containLabel: true
                        },
                        legend: {
                            top: 0,
                            textStyle: {
                                color: "#fff",
                            },
                            itemWidth: 10,  // 设置宽度
                            itemHeight: 10, // 设置高度
                        },
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                            }
                        },
                        xAxis: {
                            type: 'category',
                            data: titlename,
                            axisTick: { //---坐标轴 刻度
                                show: true, //---是否显示
                            },
                            axisLine: { //---坐标轴 轴线
                                show: true, //---是否显示
                                lineStyle: {
                                    color: 'rgba(255,255,255,.1)',
                                    width: 1,
                                    type: 'dotted',
                                },
                            },
                            axisLabel: {//X轴文字
                                rotate: -15,
                                textStyle: {
                                    fontSize: 8,
                                    color: '#fff'
                                },
                            },
                        },
                        yAxis: {
                            type: 'value',
                            splitLine: {//分割线
                                show: true,
                                lineStyle: {
                                    color: 'rgba(255,255,255,.1)',
                                    width: 1,
                                    type: 'dotted'
                                }
                            },
                            axisLabel: {//Y轴刻度值
                                formatter: '{value}',
                                textStyle: {
                                    fontSize: 12,
                                    color: '#fff'
                                },
                            },
                            axisLine: { //---坐标轴 轴线
                                show: false, //---是否显示
                            },
                        },
                        series: [{
                            name: '酒店数量',
                            type: 'bar',
                            data: data,
                            barWidth: 15,
                            barGap: 1, //柱子之间间距 //柱图宽度      两种情况都要设置，设置series 中对应数据柱形的itemStyle属性下的emphasis和normal的barBorderRadius属性初始化时候圆角  鼠标移上去圆角
                            itemStyle: {
                                normal: {
                                    barBorderRadius: 50,
                                    color: "#446ACF",
                                }
                            },
                        }]
                    };
                    console.log(response.data)


                    // 使用刚指定的配置项和数据显示图表。
                    myChart4.setOption(option);
                    window.addEventListener("resize", function () {
                        myChart.resize();
                    });
                }
            });
        }
    }

    //完成 星级占比
    function echarts_5(keys = "", condition = "全国") {
        // 基于准备好的dom，初始化echarts实例
        myChart5 = echarts.init(document.getElementById('echart5'));
        if (condition == "全国") {
            request_grade("/grade")//默认全国
        } else {
            url = "/grade?" + keys + "=" + condition
            request_grade(url)
        }


        function request_grade(url) {
            $.ajax({
                type: "GET",
                url: url,
                data: "{}",
                dataType: "JSON",
                success: function (response) {
                    option = {
                        legend: {
                            orient: 'vertical',
                            itemWidth: 10,
                            itemHeight: 10,
                            textStyle: {
                                color: 'rgba(255,255,255,.5)'
                            },
                            top: '1%',
                            left: 190,
                            data: Object.keys(response.data)
                        },
                        color: ['#37a2da', '#32c5e9', '#9fe6b8', '#ffdb5c', '#ff9f7f', '#fb7293', '#e7bcf3', '#8378ea'],
                        tooltip: {
                            trigger: 'item',
                            formatter: "{b} : {c} ({d}%)"
                        },

                        calculable: true,
                        series: [
                            {

                                type: 'pie',
                                radius: [20, 70],
                                center: ["50%", "60%"],
                                roseType: 'area',
                                data: data = Object.keys(response.data).map(key => {
                                    return {value: response.data[key], name: key};
                                }),
                                //        label: {
                                //        normal: {
                                //            formatter: function(param) {
                                //                return param.name +':\n' + param.value +'\n';
                                //            }

                                //        }
                                //    },
                                labelLine: {
                                    normal: {
                                        length: 3,
                                        length2: 6,//修改长度
                                        lineStyle: {width: 1}
                                    }
                                },

                                itemStyle: {
                                    normal: {
                                        shadowBlur: 30,
                                        shadowColor: 'rgba(0, 0, 0, 0.4)'
                                    }

                                },
                            }
                        ]
                    };
                    myChart5.setOption(option);
                    window.addEventListener("resize", function () {
                        myChart.resize();
                    });
                }

            });
        }

    }

    //完成 设施配备
    function echarts_6(keys = "", condition = "全国") {
        // 基于准备好的dom，初始化echarts实例
        myChart6 = echarts.init(document.getElementById('echart6'));
        if (condition == "全国") {
            request_radar("/radar")//默认全国
        } else {
            url = "/radar?" + keys + "=" + condition
            request_radar(url)
        }


        function request_radar(url) {
            $.ajax({
                type: "GET",
                url: url,
                data: "{}",
                dataType: "JSON",
                success: function (response) {
                    const names = response.data.map(item => item[0]);
                    option = {
                        tooltip: {
                            trigger: 'axis'
                        },
                        radar: [{
                            indicator: names.map(name => {
                                return {text: name, max: response.data.maxNum};
                            }),
                            textStyle: {
                                color: 'red'
                            },
                            center: ['50%', '50%'],
                            radius: '70%',
                            startAngle: 90,
                            splitNumber: 4,
                            shape: 'circle',

                            name: {
                                padding: -5,
                                formatter: '{value}',
                                textStyle: {

                                    color: 'rgba(255,255,255,.5)'
                                }
                            },
                            splitArea: {
                                areaStyle: {
                                    color: 'rgba(255,255,255,.05)'
                                }
                            },
                            axisLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.05)'
                                }
                            },
                            splitLine: {
                                lineStyle: {
                                    color: 'rgba(255,255,255,.05)'
                                }
                            }
                        },],
                        series: [{
                            name: '雷达图',
                            type: 'radar',
                            tooltip: {
                                trigger: 'item'
                            },
                            data: [{
                                name: '数值',
                                value: response.data.map(item => item[1]),
                                lineStyle: {
                                    normal: {
                                        color: '#03b48e',
                                        width: 2,
                                    }
                                },
                                areaStyle: {
                                    normal: {
                                        color: '#03b48e',
                                        opacity: .4
                                    }
                                },
                                symbolSize: 0,

                            },]
                        },]
                    };
                    myChart6.setOption(option);
                    window.addEventListener("resize", function () {
                        myChart.resize();
                    });
                }
            });
        }
    }
})


















