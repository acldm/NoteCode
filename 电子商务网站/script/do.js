window.onload = () => {
    let to_top = document.getElementById("to_top")
    to_top.onclick = function(e) {
        window.scrollTo(0, 0)
    }
}