// 选取元素时添加一个元素属性
function add_mark($elem,key,value){
    $elem[key]=value;
    return $elem;
}

// 获取同级后面某标签
function latest_elem($elem, tag_name) {
    if ($elem.next()[0].tagName == tag_name){
        return $elem.next();
    }
    else {return latest_elem($elem.next(),tag_name);}
}

// 改变最近一个标签的text跟css颜色提示信息样式
function change_css($elem,text,color) {
    var $p_elem=latest_elem($elem,'P');
    $p_elem.text(text).css({color:color});
}

// 回车切换至数组下一个input，最后一个聚焦提交
function enter_cut($elem_array,$submit_elem){
    $.each($elem_array,function (i) {
         if (i<($elem_array.length-1)){
            this['next_input'] = $elem_array[i+1];
            $elem_array[i].keypress(function () {
                if(event.keyCode == 13){
                    $elem_array[i]['next_input'].focus();
                }
            })
         }
         else{
             this.keypress(function () {
                 if (event.keyCode == 13) {
                    $submit_elem.focus()}
             })
            }
    })
}

// 让对应标签（p）的text以及颜色
function change_tips($elem,text,color){
    $elem.text(text).css({color:color});
}