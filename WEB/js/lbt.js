class lbt {
    constructor(id, img_src_list, options) {
        this.c = document.getElementById(id)
        this.img_src_list = img_src_list
        this.createHotBtn()

        this.ul_class = 'ul_class' in options ? options['ul_class'] : ''
    }

    createHotBtn() {
        
    }
}