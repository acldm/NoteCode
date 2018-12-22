class Silder {
    constructor(container, animate) {
        this.container = container
        this.gallery = this.container.getElementsByTagName("ul")[0]
        this.gallery_items = this.gallery.children
        this._index = 0
        this.events = {}
        let animate_func = animate || Silder.Animate.Normal
        let bd = animate_func(this.gallery)
        this.listener(bd.callback, bd.event)
        this.bind()
    }

    bind() {
        this.container.addEventListener("mouseover", (e) => {
            this.notice("Hover")
        })

        this.container.addEventListener("mouseout", (e) => {
            this.notice("Out")
            console.log("out")
        })
    }

    addPlugin(plugin) {
        //plugin:特殊的对象,键值对
        let bds = plugin(this)
        for (let event in bds) {
            this.listener(bds[event], event)
        }
    }

    listener(callback, event) {
        if (!(event in this.events)) {
            this.events[event] = []
        }
        this.events[event].push(callback)
    }

    notice(event, options) {
        if (!(event in this.events)) {
            return
        }

        for (let e of this.events[event]) {
            e(options)
        }
    }

    get Index() {
        return this._index
    }

    set Index(value) {
        let oldElem = this.gallery_items[this.Index]
        oldElem.Index = this.Index
        this._index = value % this.gallery_items.length
        
        let newElem = this.gallery_items[this.Index]
        newElem.Index = this.Index

        this.notice("change", {
            oldElem: oldElem,
            newElem: newElem
        })
    }

}

//动画效果,指定列表的初始表现,只用于操作ul列表,监听Change事件,传递一个可配置对象
Silder.Animate = {}
Silder.Animate.Normal = function(gallery) {
    console.log(gallery.classList)
    gallery.classList.add("silder-normal")
    gallery.style.left = "0px"
    let gallery_length = gallery.children.length

    let child_width = gallery_length > 0 ? gallery.children[0].offsetWidth : 0
    if (gallery_length > 0) {
        gallery.children[0].style.opacity = '1'
    }

    return {
        callback: function(options) {
            let nowIndex = options.newElem.Index
            gallery.style.left = `-${nowIndex * child_width}px`
            console.log(child_width)
        },
        event: 'change'
    }
}

let AutoPlay = function (delta_time) {
    let timer = null
    let silder = null
    let start = function () {
        stop()
        timer = setInterval(() => {
            silder.Index += 1
        }, delta_time)

    }

    let stop = function() {
        clearInterval(timer)
    }

    start()

    return function plugin(s) {
        silder = s
        return {
            "Hover": stop,
            "Out": start,
        }
    }
}

let HotBtn = function () {

}