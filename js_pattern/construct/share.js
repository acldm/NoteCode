/**
 * 共享模式
 * 核心思想: 将需要复用的属性方法全部放在原型中,这样就不需要this的内容了
 */

function inherit(C, P) {
    //子类原型指向父类原型
    C.prototype = P.prototype
}

function Parent() {

}

Parent.prototype.name = "linda"
Parent.prototype.getName = function() {
    return Parent.prototype.name
}

function Child() {

}

inherit(Child, Parent)
let kid = new Child()
console.log(kid.getName())