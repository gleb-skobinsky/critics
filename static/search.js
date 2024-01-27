function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

function appendParams(searchQuery) {
    let url = new URL(window.location.href);
    url.searchParams.set('query', searchQuery);
    window.history.replaceState(null, null, url);
}

function populateSearchResults(results) {
    let resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHtml = "";
    for (const result of results) {
        console.log(result);
        resultsContainer.innerHTML += `<div class="column is-6 is-article-entry">
                <div class="article-title">
                    <div class="columns is-vcentered">
                        <div class="column">
                            <div class="one-weekly-title">${result.heading}</div>
                        </div>
                        <div class="column is-narrow">
                            <span class="dot"></span>
                        </div>
                    </div>
                </div>
                <a href="${result.post_url}" class="imgart-wrapper">
                    <img class="article-image" src="/media/${result.cover_image}"/>
                </a>
            </div>`
    }
}

function sendSearchQuery() {
    let query = document.getElementById("search-field").value;
    if (!isBlank(query)) {
        appendParams(query);
        fetch(`/search-query?query=${query}`)
            .then(response => response.text())
            .then(text => populateSearchResults(JSON.parse(text).search_results))
    }
}

function loadWindowActions() {
    let searchButton = document.getElementById("do-search");
    searchButton.addEventListener("click", sendSearchQuery, false);
}

window.addEventListener("load", loadWindowActions, false);