/**
 * 地区联动
 * */
function getProvince(){
	$("#shengshi").val('');
	$("#msg_div").empty();
	var province=eval(proStr);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	for(var i=0,psize=province.length;i<psize;i++){
		province[i].NAME;
		newStr.push("<li onclick=\"getCity("+i+")\">"+province[i].NAME+"</li>");//省
	}
	newStr.push("</ul>");
	$("#sheng_div").html(newStr.join(""));
	$("#sheng_div").css('display','block');//显示sheng的div；
	$("#shi_div").css('display','none');//隐藏shi的div；
	$("#qu_div").css('display','none');//隐藏qu的div；
	$("#xiao_div").css('display','none');//隐藏xiao的div
	$("#ban_div").css('display','none');//隐藏ban的div；
}

function getCity(valPro){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:#3973ac;\">"+province[valPro].NAME+"</li>");//省
	for(var j=0,csize=city.length;j<csize;j++){
		newStr.push("<li onclick=\"getArea("+j+","+valPro+")\"  style=\"padding-left:20px;\">"+city[j].NAME+"</li>");//市
	}
	newStr.push("</ul>");
	$("#shi_div").html(newStr.join(""));

	$("#sheng_div").css('display','none');//隐藏
	$("#shi_div").css('display','block');//显示
	$("#qu_div").css('display','none');//隐藏
	$("#xiao_div").css('display','none');//隐藏
	$("#ban_div").css('display','none');//隐藏
}

function getArea(valCity,valPro){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var area=eval(city[valCity].ITEMS);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:#3973ac;\">"+province[valPro].NAME+"</li>");//省
	newStr.push("<li onclick=\"getCity("+valPro+")\" style=\"background-color:#538cc6;padding-left:10px;\">"+city[valCity].NAME+"</li>");//市
	for(var t=0,asize=area.length;t<asize;t++){
		area[t].NAME;
		newStr.push("<li  style=\"padding-left:25px;\" onclick=\"getSchool("+t+","+valCity+","+valPro+")\">"+area[t].NAME+"</li>");//区
	}
	newStr.push("</ul>");

	$("#sheng_div").css('display','none');//隐藏
	$("#shi_div").css('display','none');//隐藏
	$("#qu_div").css('display','block');//显示
	$("#xiao_div").css('display','none');//隐藏
	$("#ban_div").css('display','none');//隐藏
	//如果不存在qu
	if(asize==0){
		var allarea=province[valPro].NAME+"-"+city[valCity].NAME;
		$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":"","XX":"","BJ":""});
		$("#shengshi").val(allarea);
		$("#msg_div").html("<h3>您选择的地市还没有区县，请联系您的老师添加后再来注册。</h3>");
		$("#shengshi_submit").css('display','none');//隐藏提交按钮；
	}
	else{
		$("#qu_div").html(newStr.join(""));
	}
}

function getSchool(valArea,valCity,valPro){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var area=eval(city[valCity].ITEMS);
	var sch=eval(area[valArea].ITEMS);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:##3973ac;\">"+province[valPro].NAME+"</li>"); //省
	newStr.push("<li onclick=\"getCity("+valPro+")\" style=\"background-color:#538cc6;padding-left:10px;\">"+city[valCity].NAME+"</li>");//市
	newStr.push("<li onclick=\"getArea("+valCity+","+valPro+")\"  style=\"background-color:#8cb2d9;padding-left:10px;\">"+area[valArea].NAME+"</li>");//区
	for(var k=0,asize=sch.length;k<asize;k++){
		sch[k].NAME;
		newStr.push("<li  style=\"padding-left:25px;\" onclick=\"getClass("+k+","+valArea+","+valCity+","+valPro+")\">"+sch[k].NAME+"</li>");//校
	}
	newStr.push("</ul>");

	$("#sheng_div").css('display','none');//隐藏
	$("#shi_div").css('display','none');//隐藏
	$("#qu_div").css('display','none');//隐藏
	$("#xiao_div").css('display','block');//显示
	$("#ban_div").css('display','none');//隐藏
	if(asize==0){
		var allarea=province[valPro].NAME+"-"+city[valCity].NAME+"-"+area[valArea].NAME;
		$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":area[valArea].NAME,"XX":"","BJ":""});
		$("#shengshi").val(allarea);
		$("#msg_div").html("<h3>您选择的地区还没有学校，请联系您的老师添加后再来注册。</h3>");
		$("#shengshi_submit").css('display','none');//隐藏提交按钮；
	}
	else{
		$("#xiao_div").html(newStr.join(""));
	}
}


function getClass(valSch,valArea,valCity,valPro){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var area=eval(city[valCity].ITEMS);
	var sch=eval(area[valArea].ITEMS);
	var cla=eval(sch[valSch].ITEMS);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:#3973ac;\">"+province[valPro].NAME+"</li>"); //省
	newStr.push("<li onclick=\"getCity("+valPro+")\" style=\"background-color:#538cc6;padding-left:10px;\">"+city[valCity].NAME+"</li>");//市
	newStr.push("<li onclick=\"getArea("+valCity+","+valPro+")\"  style=\"background-color:#8cb2d9;padding-left:10px;\">"+city[valCity].NAME+"</li>");//区
	newStr.push("<li onclick=\"getSchool("+valArea+","+valCity+","+valPro+")\"  style=\"background-color:#d9e6f2;padding-left:10px;\">"+sch[valSch].NAME+"</li>");//校
	for(var q=0,asize=cla.length;q<asize;q++){
		cla[q].NAME;
		newStr.push("<li  style=\"padding-left:25px;\" onclick=\"getallArea("+q+","+valSch+","+valArea+","+valCity+","+valPro+")\">"+cla[q].NAME+"</li>");//班
	}
	newStr.push("</ul>");

	$("#sheng_div").css('display','none');//隐藏
	$("#shi_div").css('display','none');//隐藏
	$("#qu_div").css('display','none');//隐藏
	$("#xiao_div").css('display','none');//隐藏
	$("#ban_div").css('display','block');//显示
	if(asize==0){
		var allarea=province[valPro].NAME+"-"+city[valCity].NAME+"-"+area[valArea].NAME+"-"+sch[valSch].NAME;
		$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":area[valArea].NAME,"XX":sch[valSch].NAME,"BJ":""});
		$("#shengshi").val(allarea);
		$("#msg_div").html("<h3>您选择的学校还没有班级，请联系您的老师添加后再来注册。</h3>");
		$("#shengshi_submit").css('display','none');//隐藏提交按钮；
	}
	else{
		$("#ban_div").html(newStr.join(""));
	}
}

function getallArea(valCla,valSch,valArea,valCity,valPro){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var area=eval(city[valCity].ITEMS);
	var sch=eval(area[valArea].ITEMS);
	var cla=eval(sch[valSch].ITEMS);
	var allarea=province[valPro].NAME+"-"+city[valCity].NAME+"-"+area[valArea].NAME+"-"+sch[valSch].NAME+"-"+cla[valCla].NAME;
	$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":area[valArea].NAME,"XX":sch[valSch].NAME,"BJ":cla[valCla].NAME});
	$("#shengshi").val(allarea);
	$("#province").val(province[valPro].NAME);
	$("#city").val(city[valCity].NAME);
	$("#district").val(area[valArea].NAME);
	$("#school").val(sch[valSch].NAME);
	$("#class").val(cla[valCla].NAME);
	$("#sheng_div").css('display','none');//隐藏sheng的div；
	$("#shi_div").css('display','none');//隐藏shi的div；
	$("#qu_div").css('display','none');//隐藏qu的div；
	$("#xiao_div").css('display','none');//隐藏xiao的div
	$("#ban_div").css('display','none');//隐藏ban的div；
	$("#shengshi_submit").css('display','block');//显示提交按钮的div；
}

/*地区联动*/