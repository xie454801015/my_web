var warp_slide = document.getElementById("main_wrapper");
    background_img = warp_slide.getElementsByTagName("img")[0];
    picture_box = warp_slide.getElementsByTagName("ul")[0];
    jpg_url = picture_box.getElementsByTagName("img");
    cut_div = warp_slide.getElementsByClassName("cut_button");
    message_ul = warp_slide.getElementsByTagName("div")[2].getElementsByTagName("li");
    message_text = warp_slide.getElementsByTagName("div")[3].getElementsByTagName("a");

// 控制变量对象构建
var controls = {
        pic_number : message_text.length,
        present_value:0,
        target_value:0,
        time_size:3000,
        timing_iid:"",
        // timing_tid:"",
        flagI:true,
        // flagT:false,
        cut_key:false,
        setTimers:function(){
            controls.flagI = true;
            controls.timing_iid = setInterval("rotateS()",controls.time_size);
        },
        clearTimer:function(){
             clearInterval(controls.timing_iid);
             controls.flagI = false;
             //中止轮播
        },
        cutLast:function (e) {
            stopBubble(e);
            controls.target_value--;
            controls.flagI = true;
            controls.cut_key = true
            setTimeout("rotateS()",200)
        },
        cutNext:function (e) {
            stopBubble(e);
            controls.target_value++;
            controls.flagI = true;
            controls.cut_key = true
            setTimeout("rotateS()",200)
        },
    };
//图片切换
function switchOver(number) {
    picture_box.style.left = (number)*(-1100)+"px";
    background_img.src = jpg_url[number].src;
    message_ul[number].id = "selected";
    message_ul[controls.present_value].id = "";
    message_text[number].id = "showed";
    message_text[controls.present_value].id = "";
    controls.present_value = number;
}
//轮播逻辑主体
function rotateS() {
    if(controls.flagI) {
        if(controls.cut_key)
            {
                controls.flagI = false;
                controls.cut_key = false;
            }
        else{controls.target_value++;}

        if (controls.target_value >controls.pic_number-1) {
            controls.target_value = 0;
        }
        else if (controls.target_value < 0) {
            controls.target_value = controls.pic_number - 1;
        }
        // console.log(controls.target_value);
        switchOver(controls.target_value);
    }
}
//获取mouse移动事件元素变动
var EventUtil = {
    getEvent:function (event) {
        return event? event:window;
    },
    getTarget:function(event){
        event = EventUtil.getEvent(event);
        // console.log(event.target || event.srcElement);
        return event.target || event.srcElement;
    },
    getRelatedTarget:function (event) {
        event = EventUtil.getEvent(event);
        if(event.relatedTarget){
            return event.relatedTarget;
        }else if (event.type == "mouseout" )
            { return event.toElement;
            }
        else if (event.type == "mouseover"){
            return event.fromElement;
        }else {
            return null;
        }
    },
    // 元素父子判断
    judgeRelation:function (element,event) {
            var temp_related_target = EventUtil.getRelatedTarget(event);
            while(temp_related_target)
            {if (temp_related_target == element){return true;}
            else{ temp_related_target = temp_related_target.parentNode;}}
    },
}

//清除事件冒泡
function stopBubble(event){
    // console.log(event);
    if(event.stopPropagation){
        event.stopPropagation();
    }else{
        event.cancelBubble = true;
    }
}
function overEvent(e){

    if(!EventUtil.judgeRelation(this,e)){
        console.log("over");
        controls.clearTimer();

    }
}
function outEvent(e){
     if(!EventUtil.judgeRelation(this,e)){
         console.log("out");
        controls.setTimers();
    }
}
//事件绑定
controls.setTimers();
warp_slide.onmouseover = overEvent;
warp_slide.onmouseout = outEvent;
cut_div[0].onclick = controls.cutLast;
cut_div[1].onclick = controls.cutNext;
