document.getElementById("uploadBtn").addEventListener("change", function() {
    // Автоматически отправляем форму при выборе файла
    document.getElementById("uploadForm").submit();
});




const loadMoreBlock = document.querySelector('._load-more')
const windowHeight = document.documentElement.clientHeight


function loadMore() {
    const loadMoreBlockPos = loadMoreBlock.getBoundingClientRect().top + pageYOffset;
    const loadMoreBlockHeight = loadMoreBlock.offsetHeight;
    if (pageYOffset > (loadMoreBlockPos + loadMoreBlockHeight) - windowHeight) {
        getContent()
    }
}

async function getContent() {
    if (!document.querySelector('._loading-icon')) {
        loadMoreBlock.insertAdjacentHTML(
            'beforeend',
            `<div class = "_loading-icon"`
        )
    }
    loadMoreBlock.classList.add('_loading');
    let response = await fetch('_more.html',{
        method: 'GET',
    });
    if (response.ok) {
        let result = await response.text();
        loadMoreBlock.insertAdjacentHTML('beforeend',result);
        loadMoreBlock.classList.remove('_loading');
        if (document.querySelector('_loading-icon')) {
            document.querySelector('._loading-icon').remove();
        }
    }else {
        alert('Error');
    }
}