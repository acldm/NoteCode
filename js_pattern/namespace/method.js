if (Function.prototype.method !== 'function') {
    Function.prototype.method = function(name, func) {
        this.prototype[name] = func
        return this
    }
}

let a = (function () {
    this.name = "linda"
}).method("getName", function() {
    return this.name
})

let ox = new a()
console.log(ox.getName())