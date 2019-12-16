var perPage = 20;
var numPage = 1;
function genTables() {
    var tables = document.querySelectorAll(".pagination-table");
    tables.forEach( table => {
        perPage = parseInt(table.dataset.pagecount);
        createPaginator(table)
        showRow(table)
    })
}

function createPaginator(table){
    listTR = Array.from(table.getElementsByTagName('tr'))
    nbPage = Math.ceil(listTR.length/perPage)
    let paginator = document.createElement("div")
    for(var i = 1; i <= nbPage; i++){
        pageItem = document.createElement("span")
        pageItem.textContent = ""+i
        pageItem.dataset.itemIndex = i 
        pageItem.classList = "paginator-item"
        if(i == 1)
            pageItem.classList.add("paginator-selected-item")
        pageItem.addEventListener('click', clickIndexItem)
        pageItem.table = table
        paginator.appendChild(pageItem)
    }
    paginator.classList = "paginator"
    console.log(paginator)
    table.parentElement.insertBefore(paginator, table); 
}


function clickIndexItem(evt){
    Array.from(document.getElementsByClassName('paginator-selected-item')).forEach(item => {
        item.classList.remove('paginator-selected-item')
    })
    this.classList.add("paginator-selected-item")
    numPage = this.dataset.itemIndex
    showRow(evt.currentTarget.table)
}

function showRow(table){
    
    listTR = Array.from(table.getElementsByTagName('tr'))

    Array.from(listTR).forEach( (elem, index) => {
        listTR[index].classList.add("hidden-row")
        if(index >= (numPage-1)*perPage && index < numPage*perPage)
            listTR[index].classList.remove("hidden-row")
    })

    // for(index = (numPage-1)*perPage; index < numPage*perPage ; index++){
    //     if(index < listTR.length)
    //         listTR[index].classList.toggle("hidden-row")
    //     else
    //         break
    // }
}

window.addEventListener('load', function() {
    genTables();
});