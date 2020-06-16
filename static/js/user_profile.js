const menu = document.getElementById("menu-user");
const a_menu = menu.getElementsByTagName("a");

Array.from(a_menu).forEach(link => {
    // console.log(link)
    // console.log(link.hash)
    // console.log(link.classList)
    link.addEventListener("click", function() {
        console.log(this)
        if(!this.classList.contains("is-active")){
            let actual_link = menu.getElementsByClassName("is-active")[0];
            let actual_link_hash = actual_link.hash.replace("#", ""); 
            document.getElementById(actual_link_hash).classList.add("user-section-hidden")
            actual_link.classList.remove("is-active");

            this.classList.add("is-active")
            document.getElementById(this.hash.replace("#", "")).classList.remove("user-section-hidden");
        }
    })
});