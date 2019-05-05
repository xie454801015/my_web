// 由于外部JS无法直接获取django传递的数据（可内script部分优先获取变量值，但这会增加前后端代码交织过多，并容易泄露数据）直接在页面加载完全，发送一个异步请求获取数据，进而创建相关div完成布局

window.onload = function () {
    var elm = new Vue({
        delimiters:["{[", "]}"],
        el:'#table_wrapper',
        data: {
            block_name:'aaaa',
            articles:[],
        },
        methods:{
            post_ajax:function () {
                this.$http.post('',{csrfmiddlewaretoken: getCookie('csrftoken'),page_no:'1',},{emulateJSON:true}).then(function(res){
                    this.block_name = res.body.block_name;
                    this.articles = eval(res.body.articles);
                });
            }
        }
    })
    elm.post_ajax();
};

function getCookie(name){
    //获取cookie函数
    name = name + "=";
    var start = document.cookie.indexOf(name),
        value = null;
    if(start>-1){
        var end = document.cookie.indexOf(";",start);
        if(end == -1){
            end = document.cookie.length;
        }
        value = document.cookie.substring(start+name.length,end);
    }
    return value;
}