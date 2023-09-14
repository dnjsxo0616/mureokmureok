function toggleSearchButton(input) {
    var firstSpan = document.getElementById("firstSpan");
    var secondParagraph = document.getElementById("secondParagraph");
    var thirdParagraph = document.getElementById("thirdParagraph");
    var searchButton = document.getElementById("searchButton");
    if (input.value.trim() !== "") {
        firstSpan.style.display = "none";
        secondParagraph.style.display = "none";
        thirdParagraph.style.display = "none";
        searchButton.style.display = "inline-block";
    } else {
        firstSpan.style.display = "inline";
        secondParagraph.style.display = "inline";
        thirdParagraph.style.display = "inline";
        searchButton.style.display = "none";
    }
}
