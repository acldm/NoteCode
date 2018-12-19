/**
 * 默认构造模式
 * 同时继承this和原型
 */

function Parent() {
    this.name = "Linda"
}

Parent.prototype.getName = function() {
    console.log(this.name)
}

function Child() {

}


//继承函数
//继承了两次,继承了this属性又继承了又继承了原型属性
function inherit(C, P) {
    C.prototype = new P()
}

inherit(Child, Parent)

let kid = new Child()
kid.name = "sam"
kid.getName()
