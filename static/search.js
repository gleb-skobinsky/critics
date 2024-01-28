function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

function appendParams(searchQuery) {
    let url = new URL(window.location.href);
    url.searchParams.set('query', searchQuery);
    url.searchParams.set('page', 1);
    window.history.replaceState(null, null, url);
}

function populateSearchResults(results, query) {
    let resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = "";
    let finalResult = "";
    for (const row of results.search_results) {
        finalResult += `<div class="columns">`
        for (const result of row) {
            finalResult += `<div class="column is-one-third is-article-entry">
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
        finalResult += "</div>"
    }
    console.log(finalResult);
    resultsContainer.innerHTML = finalResult;
    if (results.num_pages > 1) {
        let pagination = document.getElementById("pagination-holder");
        pagination.classList.remove("pagination-hidden");
        let paginationList = document.getElementById("pagination-list");
        paginationList.innerHTML = "";
        if (results.num_pages < 6) {
            let pagesRange = [...Array(results.num_pages).keys()];
            for (pageNum of pagesRange) {
                let trueNum = pageNum + 1
                let curClass = trueNum == 1 ? "is-current" : "";
                paginationList.innerHTML += `<li>
                    <a href="/search/?query=${query}&page=${trueNum}" class="pagination-link ${curClass}" aria-label="Goto page ${trueNum}">${trueNum}</a>
                </li>`
            }
        } else {
            paginationList.innerHTML += `<li>
                    <a href="/search/?query=${query}&page=1" class="pagination-link is-current" aria-label="Goto page 1">1</a>
                </li>
                <li>
                    <a href="/search/?query=${query}&page=2" class="pagination-link" aria-label="Goto page 2">2</a>
                </li>
                <li>
                    <span class="pagination-ellipsis">&hellip;</span>
                </li>
                <li>
                    <a href="/search/?query=${query}&page=${results.num_pages - 1}" class="pagination-link" aria-label="Goto page ${results.num_pages - 1}">${results.num_pages - 1}</a>
                </li>
                <li>
                    <a href="/search/?query=${query}&page=${results.num_pages}" class="pagination-link" aria-label="Goto page ${results.num_pages}">${results.num_pages}</a>
                </li>
                `
        }
    }
}

function sendSearchQuery() {
    let query = document.getElementById("search-field").value;
    if (!isBlank(query)) {
        appendParams(query);
        fetch(`/search-query?query=${query}`)
            .then(response => response.text())
            .then(text => populateSearchResults(JSON.parse(text), query))
    }
}

function getOrDefault(params, key, defaultVal) {
    let value = parseInt(params.get(key));
    if (value === null || isNaN(value)) {
        value = defaultVal;
    }
    return value
}

function goBack() {
    let url = new URL(window.location.href);
    let page = getOrDefault(url.searchParams, "page", 1);
    if (page > 1) {
        url.searchParams.set("page", page - 1);
        window.location.href = url;
    }
}

function goForward() {
    let url = new URL(window.location.href);
    let page = getOrDefault(url.searchParams, "page", 1);
    url.searchParams.set("page", page + 1);
    window.location.href = url;
}

function loadWindowActions() {
    document.getElementById("do-search").addEventListener("click", sendSearchQuery, false);
    document.getElementById("pagination-go-back").addEventListener("click", goBack, false);
    document.getElementById("pagination-go-forward").addEventListener("click", goForward, false);
}

window.addEventListener("load", loadWindowActions, false);