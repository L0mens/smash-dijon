let currentChar = 1;

const nbCharButtons = document.getElementById("nb-char-buttons")

const charImg = document.getElementsByClassName("stock-chara");

const confirmSkinButton = document.getElementById("confirm-char")

let saveCharUrl = 'https://' +window.location.host +'/rank/characters/save'
if (window.location.host == '127.0.0.1:8000') 
    saveCharUrl = 'http://' +window.location.host +'/rank/characters/save'

let char1, char2, char3, skin1, skin2, skin3 ;

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

Array.from(charImg).forEach((char) => {
    char.addEventListener('click', function(e){
        let actualCharSelect = document.getElementsByClassName(`char-select-${currentChar}`);
        console.log(actualCharSelect.length)
        if (actualCharSelect.length > 0)
            actualCharSelect[0].classList.remove(`char-select-${currentChar}`);
        this.classList.add(`char-select-${currentChar}`);

        let skinSelect = document.getElementById(`skin-select-${currentChar}`);
        skinSelect.children[0].classList.remove('hidden');
        

        var count = 0
        Array.from(skinSelect.children[0].children).forEach((skinImg) => {
            skinImg.src = `/static/img/stockimg/chara_2_${this.alt}_0${count}.png`;
            count++;
            skinImg.addEventListener('click', function() {
                let num = (this.parentNode.parentNode.id).split('-')[2]
                let actualCharSelect = document.getElementsByClassName(`skin-selected-${num}`);
                console.log(actualCharSelect.length)
                if (actualCharSelect.length > 0)
                    actualCharSelect[0].classList.remove(`skin-selected-${num}`);
                this.classList.add(`skin-selected-${num}`);
            })
        })
    })
})

confirmSkinButton.addEventListener('click', function(e){
    e.preventDefault();
    var elo = document.getElementById("player_elo");
    var idElo = elo.value;
    sendData = {
        "id_elo" : idElo
    }
    char1 = document.getElementsByClassName('char-select-1')[0]
    char2 = document.getElementsByClassName('char-select-2')[0]
    char3 = document.getElementsByClassName('char-select-3')[0]
    skin1 = document.getElementsByClassName('skin-selected-1')[0]
    skin2 = document.getElementsByClassName('skin-selected-2')[0]
    skin3 = document.getElementsByClassName('skin-selected-3')[0]
    data = []
    if (char1 != undefined)
        data[0] = {"name" : char1.alt , "skin" : parseInt(skin1.alt)}
    if (char2 != undefined)
        data[1] = {"name" : char2.alt , "skin" : parseInt(skin2.alt)}
    if (char3 != undefined)
        data[2] = {"name" : char3.alt , "skin" : parseInt(skin3.alt)}
    sendData["char"] = data;

    const reset = document.getElementById('reset-check')
    sendData["reset"] = reset.checked
    fetch(saveCharUrl, {
        method: 'POST',
        body: JSON.stringify(sendData),
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    })
    .then(data =>{return data.json();})
    .then(res=>{
        console.log(res)
    })
});
