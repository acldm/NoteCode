/**
 * 借用构造函数模式
 * 继承this，无法继承原型
 */

function Article(title) {
    this.title = title || "null"
}

Article.prototype.getTitle = function () {
    console.log(this.title)
}

function BlogPost(title) {
    //在子构造函数中直接以函数形式调用父类构造函数
    Article.apply(this, arguments)
}

let post = new BlogPost('sams')
console.log(BlogPost.prototype.constructor)
console.log(post.title)
console.log(post.getTitle)