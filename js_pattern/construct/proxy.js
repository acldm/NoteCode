/**
 * 临时构造函数模式
 * 切断子对象与父对象之间的直接连接关系
 */

let inherit = (function() {
    let F = function() {}
    return function (C, P) {
        F.prototype = P.prototype
        C.prototype = new F()
        //标识子类的父类
        C.uber = P.prototype
        //若不改变构造函数指针，则原始指向Parent
        C.prototype.constructor = C
    }
}())

function Parent () {
    this.name = "Linda"
}

Parent.prototype.getName = function () {
    console.log(this.name)
}

function Child() {

}

inherit(Child, Parent)
let kid = new Child()
kid.name = "sam"
kid.getName()
console.log(Child.prototype.constructor)