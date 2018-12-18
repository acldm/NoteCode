let MYAPP = {}

MYAPP.namespace = function(ns_string) {
    let parts = ns_string.split('.')

    let parent = MYAPP
    if (parts[0] == 'MYAPP') {
        parts.slice(0)
    }

    for (let i = 0; i < parts.length; i++) {
        if (parent[parts[i]] == undefined) {
            parent[parts[i]] = {}
        }
        parent = parent[parts[i]]
    }

    return parent
}

module.exports = MYAPP