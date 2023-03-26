// 添加全局请求头
$(document).ajaxSend(function(event, xhr) {
	xhr.setRequestHeader('Authorization',"Bearer "+localStorage.getItem("token")); // 增加一个自定义请求头
	console.log("Bearer "+localStorage.getItem("token"))
});

