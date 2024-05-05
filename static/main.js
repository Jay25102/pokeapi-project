BASE_API = "https://pokeapi.co/api/v2/";
const input = document.querySelector("#pokemon-search");
const suggestions = document.querySelector(".suggestions ul");
const searchForm = document.querySelector("#search-form");
const pkmnTeamDiv = document.querySelector("#pokemon-team-div");
const finishTeamBtn = document.querySelector("#finish-team");
let pkmnList;
let pkmnNameList = [];
let pkmnTeam = [];
let numPkmn = 0;

/* 
    Search bar stuff
*/

function search(str) {
    // returns array of search results
    let results = [];
    results = pkmnNameList.filter(val => {
        return val.toLowerCase().includes(str.toLowerCase());
    });
    return results;
}

function hideSuggestions() {
    // hiding ils when appropriate
    while (suggestions.firstChild) {
        suggestions.removeChild(suggestions.firstChild);
    }
}

function searchHandler(e) {
    showSuggestions(search(input.value), input.value);
}

function showSuggestions(results, inputVal) {
    hideSuggestions();
    // showing lis when appropriate

    if (inputVal === "") {
        return;
    }

    results.forEach(val => {
        const newLi = document.createElement("li");
        newLi.innerText = val;
        suggestions.append(newLi);
    });
}

function useSuggestions(e) {
    // fills the input with suggestions
    if (e.target.tagName == "LI") {
        input.value = e.target.innerText;
        hideSuggestions();
    }
}

input.addEventListener('keyup', searchHandler);
suggestions.addEventListener('click', useSuggestions);


/* 
    Pokemon stuff
*/

async function getPokemonList() {
    // gets a list of all pokemon from pokeapi
    // limit is 1350 because there are only about 1300 pokemon
    response = await axios.get(`${BASE_API}/pokemon?limit=1350`);
    return response;
}

function addPokemonToTeam(name, url) {
    // create a json object with name:url and add it to global pkmnTeam arr
    let singlePkmn = [];
    singlePkmn[0] = name;
    singlePkmn[1] = url;
    console.log(singlePkmn);
    pkmnTeam.push(singlePkmn);
}

finishTeamBtn.addEventListener("click", async function(e) {
    // when button is pressed, send the arr of json objects to flask
    e.preventDefault();
    for (let i = pkmnTeam.length; i < 6; i++) {
        pkmnTeam.push(["",""]);
    }
    // console.log(pkmnTeam);
    await axios.post("/teams/new", pkmnTeam);
    console.debug("DEBUG: sent team to server");
    location.reload();
});

function getPokemonNameList(pkmnList) {
    // trim down the list to only have names
    let pkmnNameList = [];
    let names = pkmnList.data.results;
    for (let i = 0; i < names.length; i++) {
        pkmnNameList.push(names[i].name);
    }
    return pkmnNameList;
}

function searchForURL(pkmnName) {
    // finds the pokemon's associated url
    let pkmnURL;
    if (pkmnNameList.indexOf(pkmnName) === -1) {
        return -1;
    }
    
    for (let i = 0; i < pkmnList.data.results.length; i++) {
        if (pkmnList.data.results[i].name === pkmnName) {
            pkmnURL = pkmnList.data.results[i].url;
        }
    }

    return pkmnURL;
}

async function getPokemonSprite(pkmnURL) {
    // uses the associated url to get the front facing sprite (image)
    let response = await axios.get(pkmnURL);
    // console.log(response.data.sprites.front_default);
    return response.data.sprites.front_default;
}

searchForm.addEventListener("submit", async function(e) {
    // adds a pokemon to the temporary list
    // this feels like the long way around since we already have a list of pokemon names
    e.preventDefault();
    if (numPkmn === 6) {
        alert("Max six pokemon in a team!");
        return -1;
    }
    let pkmnName = input.value;
    let pkmnURL = searchForURL(pkmnName);
    if (pkmnURL === -1) {
        alert("Incorrect Pokemon name, try again");
    }
    else {
        let spriteURL = await getPokemonSprite(pkmnURL);
        newDiv = document.createElement("div");
        newDiv.classList.add("card");
        newDiv.innerHTML += `<div>${pkmnName}</div>`;
        newDiv.innerHTML += `<img src="${spriteURL}" alt="${pkmnName}">`;
        pkmnTeamDiv.appendChild(newDiv);
        addPokemonToTeam(pkmnName, spriteURL);
        numPkmn++;
    }
    input.value = "";
});

/* 
    Starting stuff
*/

async function start() {
    // starting function once page loads
    console.debug("DEBUG: finished loading");
    pkmnList = await getPokemonList();
    pkmnNameList = getPokemonNameList(pkmnList);
    // console.log(pkmnNameList);
}

document.addEventListener("DOMContentLoaded", start);