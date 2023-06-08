const noticeImageInput = document.getElementById("photo");
const noticeImagePreview = document.getElementById("preview");

if (noticeImageInput) {
    noticeImageInput.addEventListener("change", function () {
        const file = this.files[0];
        const reader = new FileReader();
        reader.addEventListener("load", function () {
            noticeImagePreview.src = reader.result;
            noticeImagePreview.style.display = "block";
        });
        reader.readAsDataURL(file);
    });
}  