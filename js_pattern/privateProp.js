let obj = (function() {
    let id = 0
    return function() {
        console.log(`current new obj id: ${id}`)
        if (this instanceof arguments.callee) {
            id++            
        }
    }
}())

new obj()
new obj()
new obj()