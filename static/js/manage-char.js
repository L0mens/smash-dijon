let currentChar = 1;

const nbCharButtons = document.getElementById("nb-char-buttons")

Array.from(nbCharButtons.children).forEach((button) =>{
    button.addEventListener('click', function(e){
        e.preventDefault();
        this.classList.remove('is-outlined')
        nbCharButtons.getElementsByClassName(`char-${currentChar}`)[0].classList.add('is-outlined')
        if (this.classList.contains('char-1')){
            currentChar = 1;
        }
        else if  (this.classList.contains('char-2')){
            currentChar = 2;
        }
        else{
            currentChar = 3;
        }
    })
})