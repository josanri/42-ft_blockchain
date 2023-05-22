
// const chainButton = document.querySelector("#chainId");
// chainButton.addEventListener("click", () => {
//     fetch("http://localhost:5000/chain");
// })

const mineButton = document.querySelector("#mineId");
mineButton.addEventListener("click", () => {
    fetch("http://localhost:5000/mine");
})