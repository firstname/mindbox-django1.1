/**
 * 地区联动
 * */
function getProvince(){
//$("body .dqld_div").remove();
	var province=eval(proStr);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	for(var i=0,psize=province.length;i<psize;i++){
		province[i].NAME;
		newStr.push("<li onclick=\"getCity("+i+")\">"+province[i].NAME+"</li>");
	}
	newStr.push("</ul>");
	//$("body").append(newStr.join(""));
	$("#sheng_div").html(newStr.join(""));
}

function getCity(valPro){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:#808080;\">"+province[valPro].NAME+"</li>");
	for(var j=0,csize=city.length;j<csize;j++){
		newStr.push("<li onclick=\"getArea("+j+","+valPro+")\"  style=\"padding-left:20px;\">"+city[j].NAME+"</li>");
	}
	newStr.push("</ul>");
	$("#shi_div").html(newStr.join(""));
	$("#sheng_div").css('display','none');//隐藏sheng的div；
}

function getArea(valCity,valPro){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var area=eval(city[valCity].ITEMS);
	var newStr=new Array();
	newStr.push("<ul class=\"_citys1\">");
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:#999999;\">"+province[valPro].NAME+"</li>");//省
	newStr.push("<li onclick=\"getCity("+valPro+")\" style=\"background-color:#ccc;padding-left:10px;\">"+city[valCity].NAME+"</li>");//市
	for(var t=0,asize=area.length;t<asize;t++){
		area[t].NAME;
		newStr.push("<li  style=\"padding-left:25px;\" onclick=\"getSchool("+t+","+valCity+","+valPro+")\">"+area[t].NAME+"</li>");//区
	}
	newStr.push("</ul>");
	if(asize==0){
		var allarea=province[valPro].NAME+city[valCity].NAME;
		$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":""});
		$("#shengshi").val(allarea);
		$("#shi_div").css('display','nonoe');
	}
	else{
		$("#sheng_div").css('display','none');//隐藏sheng的div；
		$("#shi_div").css('display','none');//隐藏shi的div；
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
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:#999999;\">"+province[valPro].NAME+"</li>"); //省
	newStr.push("<li onclick=\"getCity("+valPro+")\" style=\"background-color:#ccc;padding-left:10px;\">"+city[valCity].NAME+"</li>");//市
	newStr.push("<li onclick=\"getArea("+valCity+","+valPro+")\"  style=\"background-color:#555;padding-left:10px;\">"+area[valArea].NAME+"</li>");//区
	for(var k=0,asize=sch.length;k<asize;k++){
		sch[k].NAME;
		newStr.push("<li  style=\"padding-left:25px;\" onclick=\"getClass("+k+","+valArea+","+valCity+","+valPro+")\">"+sch[k].NAME+"</li>");//校
	}
	newStr.push("</ul>");
	if(asize==0){
		var allarea=province[valPro].NAME+city[valCity].NAME+area[valArea].NAME;
		$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":area[valArea].NAME});
		$("#shengshi").val(allarea);
		$("#shi_div").css('display','nonoe');
	}
	else{
		$("#sheng_div").css('display','none');//隐藏sheng的div；
		$("#shi_div").css('display','none');//隐藏shi的div；
		$("#qu_div").css('display','none');//隐藏qu的div；
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
	newStr.push("<li onclick=\"getProvince()\" style=\"background-color:#999999;\">"+province[valPro].NAME+"</li>"); //省
	newStr.push("<li onclick=\"getCity("+valPro+")\" style=\"background-color:#ccc;padding-left:10px;\">"+city[valCity].NAME+"</li>");//市
	newStr.push("<li onclick=\"getArea("+valCity+","+valPro+")\"  style=\"background-color:#555;padding-left:10px;\">"+city[valCity].NAME+"</li>");//区
	for(var k=0,asize=sch.length;k<asize;k++){
		sch[k].NAME;
		newStr.push("<li  style=\"padding-left:25px;\" onclick=\"getallArea("+k+","+valArea+","+valCity+","+valPro+")\">"+sch[k].NAME+"</li>");//校
	}
	newStr.push("</ul>");
	if(asize==0){
		var allarea=province[valPro].NAME+city[valCity].NAME+area[valArea].NAME;
		$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":area[valArea].NAME});
		$("#shengshi").val(allarea);
		$("#shi_div").css('display','nonoe');
	}
	else{
		$("#sheng_div").css('display','none');//隐藏sheng的div；
		$("#shi_div").css('display','none');//隐藏shi的div；
		$("#qu_div").css('display','none');//隐藏qu的div；
		$("#xiao_div").html(newStr.join(""));
	}
}

function getallArea(valPro,valCity,val2){
	var province=eval(proStr);
	var city=eval(province[valPro].ITEMS);
	var area=eval(city[valCity].ITEMS);
	var allarea=province[valPro].NAME+"-"+city[valCity].NAME+"-"+area[val2].NAME;
	$("#shengshi").attr({"SS":province[valPro].NAME,"SQ":city[valCity].NAME,"XS":area[val2].NAME});
	$("#shengshi").val(allarea);
	$("#sheng_div").css('display','none');//隐藏sheng的div；
	$("#shi_div").css('display','none');//隐藏shi的div；
	$("#qu_div").css('display','none');//隐藏qu的div；
	$("#shengshi_submit").css('display','block');//显示提交按钮的div；
}
/*地区联动*/