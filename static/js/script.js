function closeMessageOnClick(id) {
    document.querySelector(id).addEventListener("click", function() {
        this.style.display = "none"
    })
}
