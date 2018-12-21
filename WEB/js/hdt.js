class Hdt {
    constructor(id) {
        this.c = document.getElementById(id).getElementsByTagName("ul")[0]
        this.c.style.left = '0px'
        this.childs = this.c.children
        this.Timer = null
        this.init_child_width()
    }

    init_child_width() {
        if (this.childs.length <= 0) {
            this.child_width = 0
            return
        }
        let child = this.childs[0]
        let cwidth = child.offsetWidth
        this.child_width = cwidth + 12
        console.log(this.child_width)
    }

    start() {
        let childs = this.childs
        this.Timer = setInterval((function () {
            let py = parseInt(this.c.style.left)
            if (py < -this.child_width) {
                let fc = this.c.children[0]
                this.c.removeChild(fc)
                this.c.appendChild(fc)
                py = 0
            }
            this.c.style.left = `${py - 4}px`
        }).bind(this), 33)
    }

    stop() {
        clearInterval(this.Timer)
    }
}