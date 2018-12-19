function a() {
    console.log(this instanceof a)
}

a() //false
new a() //true