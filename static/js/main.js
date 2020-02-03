
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

 /*
    Page tournaments
 */
const optionsAdd = document.getElementsByClassName('option-add')
const optionsEdit = document.getElementsByClassName('option-edit')
const url = 'http://' +window.location.host +'/rank/calculate-tournament'
const editTnUrl = 'http://' +window.location.host +'/rank/reset-tournament'
const hideAddTnForm = document.getElementById('hide-form-add-tn')
console.log(hideAddTnForm)
if(hideAddTnForm){
    const formAddTn = document.getElementById('form-add-tournament')
    hideAddTnForm.addEventListener('click', function() {
        if(this.classList.contains('is-rotate')){
            this.style.transform = "rotate(0deg)";
        }
        else{
            this.style.transform = "rotate(180deg)";
        }
        formAddTn.classList.toggle('not-display');
        this.classList.toggle('is-rotate');
    })
}

var calculateCall = false;

 Array.from(optionsAdd).forEach(element => {
    element.addEventListener('click', function () {
        var tournoi = this.parentElement.parentElement.children;
        listSeason = []
        Array.from(tournoi[4].getElementsByClassName('dropdown-item')).forEach(drop => {
            listSeason.push(parseInt(drop.textContent.split("||")[0]))
        });
        var infos ={
            "name" : tournoi[0].textContent,
            "tn_slug" : tournoi[1].textContent,
            "event" : tournoi[2].textContent,
            "saison" : listSeason,
            "key" : "devtest"
        } ;
        
        if(!calculateCall){
            calculateCall = true
            fetch(url, {
                method: 'POST',
                body: JSON.stringify(infos),
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            })
            .then(data =>{return data.json();})
            .then(res=>{
                console.log(res)
                calculateCall= false
                tournoi[3].textContent = res["state"]?res["state"]:tournoi[3].textContent;
            })
        }
        
        console.log(infos)
    })
});

Array.from(optionsEdit).forEach(element => {
    element.addEventListener('click', function () {
        var tournoi = this.parentElement.parentElement.children;
        var infos ={
            "tn_slug" : tournoi[1].textContent,
            "key" : "devtest"
        } ;
        
        
        fetch(editTnUrl, {
            method: 'POST',
            body: JSON.stringify(infos),
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        })
        .then(data =>{return data.json();})
        .then(res=>{
            console.log(res)
            tournoi[3].textContent = res["state"]?res["state"]:tournoi[3].textContent;
        })
        
        
        console.log(infos)
    })
});


/* 
    Tab navigation between saison
*/

const saisontabs = document.getElementById('saison-tabs');
if(saisontabs){
    const saisontabsli = saisontabs.getElementsByTagName('li')
    Array.from(saisontabsli).forEach(li => {
        li.addEventListener('click', function() {
            if(!this.classList.contains('is-active'))
                saisontabs.getElementsByClassName('is-active')[0].classList.toggle('is-active')
                this.classList.toggle('is-active')
                var idTableRank = ("table-rank-"+this.children[0].children[0].textContent.replace(' ', '').toLowerCase())
                Array.from(document.getElementsByClassName('table-rank')).forEach(tableRank =>{
                    if(!tableRank.parentElement.classList.contains('not-display'))
                        tableRank.parentElement.classList.toggle('not-display')
                    if(tableRank.id == idTableRank)
                        tableRank.parentElement.classList.toggle('not-display')
                })
        })
    })

}

/* 
    Stage List Click
*/
const stageCard = document.getElementsByClassName('stage-card');
Array.from(stageCard).forEach((card) =>{
    card.addEventListener("click", () =>{
        card.classList.toggle("stage-selected");
    })
})

const showStageButton = document.getElementById("show-stage-check");
const figureStage = Array.from(document.getElementsByClassName("card-image"));
console.log(figureStage)
showStageButton.addEventListener('click', function() {
        
    figureStage.forEach((elt) => {
        elt.classList.toggle("hide-stage-img");
    })
        
})


