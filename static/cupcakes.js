"use strict";

const $cupcakeList = $(".cupcake-list");
const $form = $("#cupcake-form");

async function getCupcakeArray() {
  const response = await fetch(`/api/cupcakes`);

  const cupcakeData = await response.json();

  return cupcakeData.cupcakes;
}

function createCupcakeHTML(cupcake) {
  return $(`
    <div id=${cupcake.id}>
      <li>
        <p>Flavor: ${cupcake.flavor}</p>
        <p>Size: ${cupcake.size}</p>
        <p>Rating: ${cupcake.rating}</p>
      </li>
      <img src="${cupcake.image_url}"
    </div>
  `);
}

async function renderCupcake() {
  const cupcakes = await getCupcakeArray();

  for (let cupcake of cupcakes) {
    const $cupcakeHTML = createCupcakeHTML(cupcake);
    $cupcakeList.append($cupcakeHTML);
  }
}

renderCupcake();