/**
 * 借用&设置构造模式
 * 与默认模式相比，可以向父类传入构造参数
 */

function Parent(name) {
    this.name = name || "Linda"
}

Parent.prototype.getName = function() {
    console.log(this.name)
}

function Child() {
    Parent.call(this, arguments)
}

Child.prototype = new Parent()

let kid = new Child()
kid.name = "sam"
kid.getName()
//删除子类中的name后,原型链会找到父类原型中的name
delete kid.name
kid.getName()

