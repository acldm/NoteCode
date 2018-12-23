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
        })
    }

    addPlugin(plugin) {
        //plugin:特殊的对象,键值对
        console.log(plugin)
        plugin.init(this)
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

        this.notice("Change", {
            oldElem: oldElem,
            newElem: newElem
        })
    }

}

//动画效果,指定列表的初始表现,只用于操作ul列表,监听Change事件,传递一个可配置对象
Silder.Animate = {}
Silder.Animate.Normal = function(gallery) {
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
        },
        event: 'Change'
    }
}

Silder.Animate.Fade = function(gallery) {
    gallery.classList.add("silder-fade")
    return {
        callback: function(options) {
            let oldElem = options.oldElem
            let newElem = options.newElem
            oldElem.style.opacity = '0'
            newElem.style.opacity = '1'
        },
        event: 'Change'
    }
}

let AutoPlay = function (delta_time) {
    let timer = null

    let init = function (silder) {
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
        silder.listener(stop, "Hover")
        silder.listener(start, "Out")
    }

    return {
        init: init
    }
}

let HotBtn = function(btns_class) {
    btns_class = btns_class
    let btns = []
    let selectIndex = 0

    let $ = (tag) => document.createElement(tag)
    
    let create = function (items) {
        let ul = $("ul")
        btns_class ? ul.classList.add(btns_class) : 0
        Array.prototype.forEach.call(items, (v, i) => {
            btns.push($("li"))
            ul.appendChild(btns[i])
        })
        return ul
    }

    let bind = function (silder) {
        btns.forEach((b, i) => {
            b.addEventListener('click', (e) => {
                silder.Index = i
            })
        })
    }

    let Change = function (options) {
        let newIndex= options.newElem.Index
        btns[selectIndex].classList.remove("selected")
        selectIndex = newIndex
        btns[selectIndex].classList.add("selected")
    }

    return {
        init : function(silder) {
            let ul = create(silder.gallery_items)
            silder.container.appendChild(ul)
            SelectIndex = silder.Index
            btns[selectIndex].classList.add("selected")
            console.log(silder)
            bind(silder)
            silder.listener(Change, "Change")
        }
    }
}

let Nav = function (btns) {
    if (typeof btns == "string") {
        btns = document.getElementById(btns).children
    }

    let init = function(silder) {
        Array.prototype.forEach.call(btns,(b, i) => {
            b.addEventListener('mouseover', (e) => {
                silder.Index = i
            })
        })
    }

    return {
        init: init
    }

}

let EventBoard = function() {
    let board = function(msg) {
        return (options) => {
            //console.log(msg,options)
        }
    }
    
    let init = function (silder) {
        silder.listener(board("hover!"), "Hover")
        silder.listener(board("out!"), "Out")
        silder.listener(board("change!"), "Change")
    }

    return {
        init: init
    }
}