

function ShowGallery(imgs, m_img) {
    if (typeof imgs == 'string') {
        imgs = document.getElementById(imgs).children
    }

    if (typeof m_img == 'string') {
        m_img = document.getElementById(m_img)
    }

    m_img.src = imgs[0].src

    Array.prototype.forEach.call(imgs, img => {
        img.onclick = (e) => {
            m_img.src = img.src
            console.log('sss')
        }
    })
}

function NumberControll(c_id) {
    let c = document.getElementById(c_id)
    inc_btn = c.getElementsByClassName("inc-btn")[0]
    dec_btn = c.getElementsByClassName("dec-btn")[0]
    number_input = c.getElementsByTagName("input")[0]

    inc_btn.addEventListener('click', (e) => {
        let number = parseInt(number_input.value)
        number_input.value = number + 1
    })

    dec_btn.addEventListener('click', (e) => {
        let number = parseInt(number_input.value)
        if(number <= 0) {
            alert("订单数不可为负数!")
            return
        }
        number_input.value = number - 1
    })
}