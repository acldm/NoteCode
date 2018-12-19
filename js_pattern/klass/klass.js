let klass = function(P, props) {
    var Child, F
    //构造
    Child = function () {
        if (Child.uper && Child.uper.hasOwnProperty("_construct")) {
            Child.uper._construct.apply(this, arguments)
        }

        if (Child.prototype.hasOwnProperty("_construct")) {
            Child.prototype._construct.apply(this, arguments)
        }
    }

    //继承
    P = P || Object
    F = function() {}
    F.prototype = P.prototype
    Child.prototype = new F()
    
    //Chld.uper = P error! P只是构造函数,与Child是没有任何关联的
    Child.uper = P.prototype
    Child.prototype.constructor = Child

    //实现
    for (let p in props) {
        if (props.hasOwnProperty(p)) {
            Child.prototype[p] = props[p]
        }
    }

    return Child
}

let Man = klass(null, {
    _construct: function() {
        console.log("The MAN!")
        this.name = 'linda'
    },
    say: function() {
        console.log(this.name)
    }
})

let SuperMan = klass(Man, {
    _construct: function() {
        console.log("The Super Man!")
        //this.name = 'linda'
    },
})

let p = new SuperMan()
p.say()