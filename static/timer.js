

const category = document.querySelector("#category")
const timer = document.querySelector("#timer")

category.addEventListener("change", function(){
    

    fetch("/select-category", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            category_id: category.value
        })
    })
    .then(function(response) {
    return response.json();
    }) 

    .then(function(data) {
        if(data.success){
            console.log("Category chosen successfully")
        }
        else{
            console.log("Could not choose category")
        }
    });
})

let seconds = 0;

setInterval(function(){
    seconds++;
    timer.textContent = seconds;
}, 1000);