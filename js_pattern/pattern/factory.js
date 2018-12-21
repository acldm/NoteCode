function CarMaker() { }

CarMaker.prototype.driver = function () {
    console.log(this.door)
}

CarMaker.factory = function (type) {
    if (typeof CarMaker[type] !== 'function') {
        throw new Error("not constructor function!")
    }

    if (typeof CarMaker[type].prototype.driver !== 'function') {
        CarMaker[type].prototype = new CarMaker()
    }

    let car = new CarMaker[type]()
    return car
}

CarMaker.compact = function () {
    this.door = 4
}

CarMaker.SUV = function ()  {
    this.door = 6
}

let compact = CarMaker.factory("compact")
let SUV = CarMaker.factory("SUV")
compact.driver()
SUV.driver()