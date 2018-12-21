function Sale(price) {
    this.price = price || 100
}

Sale.prototype.getPrice = function () {
    return this.price
}

Sale.decorators = {}
Sale.decorators.money = {
    getPrice: function () {
        console.log(this.uper)
        return `$ ${this.uper.getPrice().toFixed(2)}`
    }
}

Sale.decorators.cdn = {
    getPrice: function () {
        return `CDN$ ${this.uper.getPrice().toFixed(2)}`
    }
}

Sale.decorators.quebce = {
    getPrice: function () {
        let price = this.uper.getPrice()
        price += price * 7.5 / 100
        return price
    }
}

Sale.prototype.decorate = function(decorator) {
    let F = function() {}
    console.log(this.constructor.decorators)
    let overrides = this.constructor.decorators[decorator]
    F.prototype = this;
    let newobj = new F()
    newobj.uper5 = F.prototype
    
    for (let i in overrides) {
        if (overrides.hasOwnProperty(i)) {
            newobj[i] = overrides[i]
        }
    }

    return newobj
}

let s = new Sale()
s = s.decorate("money")
console.log(s.getPrice())