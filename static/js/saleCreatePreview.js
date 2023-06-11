const saleImageInput = document.getElementById("photo");
const saleImagePreview = document.getElementById("preview");

if (saleImageInput) {
    saleImageInput.addEventListener("change", function () {
        const file = this.files[0];
        const reader = new FileReader();
        reader.addEventListener("load", function () {
            saleImagePreview.src = reader.result;
            saleImagePreview.style.display = "block";
        });
        reader.readAsDataURL(file);
    });
}  