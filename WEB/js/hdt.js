class Hdt {
    constructor(id) {
        this.c = document.getElementById(id).getElementsByTagName("ul")[0]
        this.c.style.left = '0px'
        this.childs = this.c.children
        this.Timer = null
    }

    start() {
        let childs =   this.childs
        this.Timer = setInterval((function() {
            let py = parseInt(this.c.style.left)
            if (py < -236) {
                let fc = this.c.children[0]
                this.c.removeChild(fc)
                this.c.appendChild(fc)
                py = 0
            }
            this.c.style.left = `${py - 2}px`
        }).bind(this), 33)
    }

    stop() {
        clearInterval(this.Timer)
    }
}